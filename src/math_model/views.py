from math_model.serializer import MetricsSerializer
from rest_framework import mixins, viewsets, status
from rest_framework.generics import get_object_or_404
from metrics.models import SupportedMetric
from measures.models import SupportedMeasure
from subcharacteristics.models import SupportedSubCharacteristic
from characteristics.models import SupportedCharacteristic
from math_model.services import MathModelServices
from rest_framework.response import Response
from pre_configs.serializers import PreConfigSerializer

class CalculateMathModelViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    #Pensei em: receber um objeto de metricas com todas as metricas coletadas, disso pego e insiro as metricas, ja retorno quando nao conseguir salvar alguma metrica
    #quando finalizar as metricas, seguir para as medidas, calcular e tentar inserir, ja apontar o erro e fazer isso para cada nivel do mdelo, ate o tsqmi
    # serializer_class = MetricsSerializer
    # metrics_queryset = SupportedMetric.objects.all()
    # measures_queryset = SupportedMeasure.objects
    # subcharacteristics_queryset = SupportedSubcharacteristic

    def create(self, request, *args, **kwargs):
        repository_id = self.kwargs['repository_pk']
        product_id = self.kwargs['product_pk']
        organization_id=self.kwargs['organization_pk']

        services = MathModelServices(repository_id, product_id, organization_id)
        product = services.get_product()
        config = product.pre_configs.first()
        serializer = PreConfigSerializer(config)
        repository = services.get_repository()
        print(serializer.data)
        services.calculate_all(request.data, repository, serializer.data)
        
        










        # serializer = MetricsSerializer(
        #     data=request.data
        # )
        # serializer.is_valid(raise_exception=True)

        # data = serializer.validated_data
        # created_at = data['created_at']

        # # 2. Get queryset
        # characteristics_keys = [
        #     characteristic['key'] for characteristic in data['characteristics']
        # ]
        # qs = SupportedCharacteristic.objects.filter(
        #     key__in=characteristics_keys
        # ).prefetch_related(
        #     'subcharacteristics',
        #     'subcharacteristics__calculated_subcharacteristics',
        # )

        # # 3. Create Core request

        # core_params = {'characteristics': []}

        # char: SupportedCharacteristic
        # for char in qs:
        #     try:
        #         subchars_params = char.get_latest_subcharacteristics_params(
        #             pre_config,
        #         )

        #     except SubCharacteristicNotDefinedInPreConfiguration as exc:
        #         return Response(
        #             {'error': str(exc)},
        #             status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        #         )

        #     core_params['characteristics'].append(
        #         {
        #             'key': char.key,
        #             'subcharacteristics': subchars_params,
        #         }
        #     )

        # calculate_result = calculate_characteristics(core_params)

        # calculated_values = {
        #     characteristic['key']: characteristic['value']
        #     for characteristic in calculate_result['characteristics']
        # }

        # # 5. Salvando o resultado

        # calculated_characteristics = []
        # repository = self.get_repository()

        # for characteristic in qs:
        #     value = calculated_values[characteristic.key]

        #     calculated_characteristics.append(
        #         CalculatedCharacteristic(
        #             characteristic=characteristic,
        #             value=value,
        #             repository=repository,
        #             created_at=created_at,
        #         )
        #     )

        # CalculatedCharacteristic.objects.bulk_create(
        #     calculated_characteristics
        # )

        # # 6. Retornando o resultado
        # serializer = LatestCalculatedCharacteristicSerializer(
        #     qs,
        #     many=True,
        #     context=self.get_serializer_context(),
        # )

        # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response("serializer.data", status=status.HTTP_201_CREATED)