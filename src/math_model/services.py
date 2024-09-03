from rest_framework.generics import get_object_or_404
from resources import calculate_measures
from measures.models import CalculatedMeasure, SupportedMeasure
from measures.serializers import (
    CalculatedMeasureHistorySerializer,
    LatestMeasuresCalculationsRequestSerializer,
    MeasuresCalculationsRequestSerializer,
    SupportedMeasureSerializer,
)
from collectors.github import utils
from collectors.github.serializers import GithubCollectorParamsSerializer
from metrics.serializers import LatestCollectedMetricSerializer
from organizations.models import Repository
from metrics.models import CollectedMetric, SupportedMetric
from measures.models import SupportedMeasure
from metrics.serializers import CollectedMetricSerializer
from utils import namefy
from rest_framework.response import Response

from collectors.sonarqube.serializers import SonarQubeJSONSerializer
from collectors.sonarqube.utils import import_sonar_metrics
from metrics.models import SupportedMetric
from organizations.models import Repository
from organizations.models import Product
from math_model.utils import parse_pre_config
    
    
class MathModelServices():     
    def __init__(self, repository_id, product_id, organization_id): 
        self.repository_id = repository_id
        self.product_id = product_id
        self.organization_id = organization_id


    def get_repository(self):
        return get_object_or_404(
            Repository,
            id=self.repository_id,
            product_id=self.product_id,
            product__organization_id=self.organization_id,
        )

    def get_product(self):
        return get_object_or_404(
            Product,
            id=self.product_id,
            organization_id=self.organization_id,
        )

    def calculate_all(self, data, repository, config): 
        # try: 
        char_keys, subchar_keys, measure_keys, metric_keys = parse_pre_config(config)
        
        metrics = self.collect_metrics(data, repository)
        for metric in metrics: 
            print("aqui ", metric.__dict__)
        measures = self.calculate_measures(
            measure_keys
        )
        # subcharacteristics = collect_subcharacteristics(
        #     measures
        # )
        # characteristics = collect_characteristics(
        #     subcharacteristics
        # )
        #SO SALVAR QUANDO TUDO DER CERTO
        saved_metrics = CollectedMetric.objects.bulk_create(metrics)
            #CollectedMetricSerializer(saved_metrics, many=True).data
        # except: 
        #     return CollectionException
        


    def collect_metrics(self, data, repository):
        
        supported_metrics = {
            supported_metric.key: supported_metric
            for supported_metric in SupportedMetric.objects.all()
        }

        collected_metrics = []
    
        for metric in data["github"]["metrics"]:
            metric_key = metric["name"]
            metric_value = metric["value"]

            if metric_key not in supported_metrics:
                return

            obj = {
                # "path": metric["path"],
                "metric": supported_metrics[metric_key],
                "value": float(metric_value),
                # "qualifier": "TRK",  # TODO FIND OUT WHAT SHOULD IT BE
            }

            in_memory_metric = CollectedMetric(**obj)
            collected_metrics.append(in_memory_metric)

        for component in data["sonarqube"]['components']:
            for obj in component['measures']:
                metric_key = obj['metric']
                metric_name = namefy(metric_key)
                metric_value = obj['value']

                if obj['metric'] not in supported_metrics:
                    supported_metrics[metric_key] = SupportedMetric.objects.create(
                        key=metric_key,
                        metric_type=SupportedMetric.SupportedMetricTypes.FLOAT,
                        name=metric_name,
                    )

                obj = {
                    'qualifier': component['qualifier'],
                    'path': component['path'],
                    'metric': supported_metrics[metric_key],
                    'value': float(metric_value),
                }

                in_memory_metric = CollectedMetric(**obj)
                collected_metrics.append(in_memory_metric)

        for collected_metric in collected_metrics:
            collected_metric.repository = repository
        
        return collected_metrics



    def calculate_measures(self, measure_keys): 
        # created_at = data['created_at']

        # 2. Obtenção das medidas suportadas pelo serviço
        measure_keys = [measure['key'] for measure in measure_keys]
        qs = SupportedMeasure.objects.filter(
            key__in=measure_keys
        ).prefetch_related(
            'metrics',
            'metrics__collected_metrics',
        )

        # 3. Criação do dicionário que será enviado para o serviço `core`
        core_params = {'measures': []}

        # 4. Obtenção das métricas necessárias para calcular as medidas

        repository = self.get_repository()

        measure: SupportedMeasure
        for measure in qs:
            metric_params = measure.get_latest_metric_params(repository)
            print("params", metric_params)

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
        # 5. Pega as configurações das thresholds
        product = self.get_product()
        pre_config = product.pre_configs.first()

        calculate_result = calculate_measures(core_params, pre_config.data)

        calculated_values = {
            measure['key']: measure['value']
            for measure in calculate_result['measures']
        }
        # 6. Salvando no banco de dados as medidas calculadas

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
                    repository=repository
                )
            )

        CalculatedMeasure.objects.bulk_create(calculated_measures)

        # 7. Retornando o resultado
        serializer = LatestMeasuresCalculationsRequestSerializer(
            qs,
            many=True
            context=self.get_serializer_context(),
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
