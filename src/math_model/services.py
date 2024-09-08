from characteristics.models import CalculatedCharacteristic, SupportedCharacteristic
from rest_framework.generics import get_object_or_404
from resources import (
    calculate_measures, 
    calculate_subcharacteristics, 
    calculate_characteristics, 
    calculate_tsqmi
)
from measures.models import CalculatedMeasure, SupportedMeasure
from organizations.models import Repository
from metrics.serializers import CollectedMetricSerializer
from metrics.models import CollectedMetric, SupportedMetric
from subcharacteristics.models import CalculatedSubCharacteristic, SupportedSubCharacteristic
from tsqmi.models import TSQMI
from tsqmi.serializers import TSQMISerializer
from utils import namefy
from utils import utils
from math_model.utils import parse_release_configuration
from release_configuration.serializers import ReleaseConfigurationSerializer
    
class MathModelServices():     
    def __init__(self, repository_id, product_id, organization_id): 
        self.repository = utils.get_repository(organization_id, product_id, repository_id)
        self.product = utils.get_product(organization_id, product_id)

    def calculate_all(self, data): 
        release_configuration = self.product.release_configuration.first()
        config_serializer = ReleaseConfigurationSerializer(release_configuration)

        char_keys, subchar_keys, measure_keys, metric_keys = parse_release_configuration(config_serializer.data) 
        metrics = self.collect_metrics(data)
        measures = self.calculate_measures(measure_keys, release_configuration)
        subcharacteristics = self.calculate_sucharacteristics(subchar_keys, release_configuration)
        characteristics = self.calculcate_characterisctics(char_keys, release_configuration)
        tsqmi = self.calculate_tsqmi(char_keys, release_configuration)
        return tsqmi


    def collect_metrics(self, data):
        supported_metrics = {
            supported_metric.key: supported_metric
            for supported_metric in SupportedMetric.objects.all()
        }

        collected_metrics = []
        if data.get("github"): 
            for metric in data["github"]["metrics"]:
                metric_key = metric["name"]
                metric_value = metric["value"]
                collected_metrics.append(
                    CollectedMetric(
                        metric=supported_metrics[metric_key],
                        value=float(metric_value),
                        repository=self.repository, 
                        qualifier="TRK"
                    )
                )
        if data.get("sonarqube"):
            for component in data["sonarqube"]['components']:
                for obj in component['measures']:
                    metric_key = obj['metric']
                    metric_name = namefy(metric_key)
                    metric_value = obj['value']

                    collected_metrics.append(
                        CollectedMetric(
                            qualifier=component['qualifier'],
                            path=component['path'], 
                            metric=supported_metrics[metric_key],
                            value=float(metric_value),
                            repository=self.repository
                        )
                    )
        print(collected_metrics)
        saved_metrics = CollectedMetric.objects.bulk_create(collected_metrics)
        serializer_metrics = CollectedMetricSerializer(
            saved_metrics, 
            many=True
        )
        
        return serializer_metrics

    def calculate_measures(self, measure_keys, release_configuration): 
        qs = SupportedMeasure.objects.filter(
            key__in=measure_keys
        ).prefetch_related(
            'metrics',
            'metrics__collected_metrics',
        )

        core_params = {'measures': []}

        measure: SupportedMeasure
        for measure in qs:
            metric_params = measure.get_latest_metric_params(self.repository)
            if metric_params:
                core_params['measures'].append(
                    {
                        'key': measure.key,
                        'metrics': [
                            {
                                "key": key,
                                "value": [float(v) for v in value] if isinstance(value, list) else [float(value)]
                            }
                            for key, value in metric_params.items()
                        ]
                    }
                )
        calculate_result = calculate_measures(core_params, release_configuration.data)

        calculated_values = {
            measure['key']: measure['value']
            for measure in calculate_result['measures']
        }

        calculated_measures = []

        measure: SupportedMeasure
        for measure in qs:
            if measure.key not in calculated_values:
                continue

            value = calculated_values[measure.key]

            calculated_measures.append(
                CalculatedMeasure(
                    measure=measure,
                    value=value,
                    repository=self.repository
                )
            )
        saved_measures = CalculatedMeasure.objects.bulk_create(calculated_measures)
        return saved_measures

    def calculate_sucharacteristics(self, subcharacteristics_keys, release_configuration): 
        qs = SupportedSubCharacteristic.objects.filter(
            key__in=subcharacteristics_keys
        ).prefetch_related(
            'measures',
            'measures__calculated_measures',
        )

        # 3. get core json response
        core_params = {'subcharacteristics': []}
        subchar: SupportedSubCharacteristic

        for subchar in qs:
            measure_params = subchar.get_latest_measure_params(release_configuration)
            core_params['subcharacteristics'].append(
                {
                    'key': subchar.key,
                    'measures': measure_params,
                }
            )

        calculate_result = calculate_subcharacteristics(core_params)

        # 4. Save data
        calculated_values = {
            subcharacteristic['key']: subcharacteristic['value']
            for subcharacteristic in calculate_result['subcharacteristics']
        }

        calculated_subcharacteristics = []

        subchar: SupportedSubCharacteristic
        for subchar in qs:
            value = calculated_values[subchar.key]

            calculated_subcharacteristics.append(
                CalculatedSubCharacteristic(
                    subcharacteristic=subchar,
                    value=value,
                    repository=self.repository
                )
            )

        saved_subchar = CalculatedSubCharacteristic.objects.bulk_create(calculated_subcharacteristics)
        return saved_subchar

    def calculcate_characterisctics(self, characteristics_keys, release_configuration): 
        qs = SupportedCharacteristic.objects.filter(
            key__in=characteristics_keys
        ).prefetch_related(
            'subcharacteristics',
            'subcharacteristics__calculated_subcharacteristics',
        )

        core_params = {'characteristics': []}

        char: SupportedCharacteristic
        for char in qs:
            subchars_params = char.get_latest_subcharacteristics_params(
                release_configuration,
            )

            core_params['characteristics'].append(
                {
                    'key': char.key,
                    'subcharacteristics': subchars_params,
                }
            )

        calculate_result = calculate_characteristics(core_params)

        calculated_values = {
            characteristic['key']: characteristic['value']
            for characteristic in calculate_result['characteristics']
        }

        calculated_characteristics = []

        for characteristic in qs:
            value = calculated_values[characteristic.key]

            calculated_characteristics.append(
                CalculatedCharacteristic(
                    characteristic=characteristic,
                    value=value,
                    repository=self.repository
                )
            )
        saved_char = CalculatedCharacteristic.objects.bulk_create(calculated_characteristics)
        return calculated_characteristics
    
    def calculate_tsqmi(self, char_keys, release_configuration): 
        characteristics_keys = [
            characteristic['key']
            for characteristic in release_configuration.data['characteristics']
        ]
        qs = (
            SupportedCharacteristic.objects.filter(
                key__in=characteristics_keys
            )
            .prefetch_related('calculated_characteristics')
            .first()
        )

        chars_params = []
        chars_params = qs.get_latest_characteristics_params(
            release_configuration,
        )

        core_params = {
            'tsqmi': {
                'key': 'tsqmi',
                'characteristics': chars_params,
            }
        }

        calculate_result = calculate_tsqmi(core_params)

        data = calculate_result.get('tsqmi')[0]

        tsqmi = TSQMI.objects.create(
            repository=self.repository,
            value=data['value']
        )
        serializer = TSQMISerializer(tsqmi)
        return serializer
