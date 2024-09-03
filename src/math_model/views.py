from math_model.serializer import MetricsSerializer
from rest_framework import mixins, viewsets, status
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
        #try:  
        services.calculate_all(request.data, repository, serializer.data)
        #except CalculateModelException as exc:
        #    return Response(
        #        {'error': str(exc)},
        #        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        #    )
        return Response("serializer.data", status=status.HTTP_201_CREATED)