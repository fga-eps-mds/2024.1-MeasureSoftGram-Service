from math_model.serializer import MetricsSerializer
from rest_framework import mixins, viewsets, status
from metrics.models import SupportedMetric
from measures.models import SupportedMeasure
from subcharacteristics.models import SupportedSubCharacteristic
from characteristics.models import SupportedCharacteristic
from math_model.services import MathModelServices
from rest_framework.response import Response
from utils.exceptions import CalculateModelException


class CalculateMathModelViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    def create(self, request, *args, **kwargs):
        repository_id = self.kwargs['repository_pk']
        product_id = self.kwargs['product_pk']
        organization_id=self.kwargs['organization_pk']

        services = MathModelServices(repository_id, product_id, organization_id)
        response = {}
        try:  
            response = services.calculate_all(request.data)
        except CalculateModelException as exc:
            return Response(
                {'error': str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(response.data, status=status.HTTP_201_CREATED)