from resources import calculate_tsqmi
from rest_framework import mixins, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from characteristics.models import SupportedCharacteristic
from measures.models import SupportedMeasure
from metrics.models import SupportedMetric
from organizations.models import Product, Repository
from tsqmi.models import TSQMI
from tsqmi.serializers import (
    TSQMICalculationRequestSerializer,
    TSQMISerializer,
)
from utils.exceptions import CharacteristicNotDefinedInReleaseConfigurationuration
from django.http import HttpResponse


class LatestCalculatedTSQMIViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = TSQMISerializer

    def get_repository(self):
        return get_object_or_404(
            Repository,
            id=self.kwargs['repository_pk'],
            product_id=self.kwargs['product_pk'],
            product__organization_id=self.kwargs['organization_pk'],
        )

    def get_queryset(self):
        repository = self.get_repository()
        return repository.calculated_tsqmis.all()

    def list(self, request, *args, **kwargs):
        repository = self.get_repository()
        latest_tsqmi = repository.calculated_tsqmis.first()
        serializer = self.get_serializer(latest_tsqmi)
        return Response(serializer.data)


class LatestCalculatedTSQMIBadgeViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = TSQMISerializer

    def get_repository(self):
        return get_object_or_404(
            Repository,
            id=self.kwargs["repository_pk"],
            product_id=self.kwargs["product_pk"],
            product__organization_id=self.kwargs["organization_pk"],
        )

    def set_stars(self, valor):
        if 0 < valor < 0.2:
            star = 1
        elif 0.2 <= valor < 0.4:
            star = 2
        elif 0.4 <= valor < 0.6:
            star = 3
        elif 0.6 <= valor < 0.8:
            star = 4
        elif 0.8 <= valor <= 1.0:
            star = 5
        else:
            star = 6
        return star

    def list(self, request, *args, **kwargs):
        repository = self.get_repository()
        latest_tsqmi = repository.calculated_tsqmis.first()
        result = self.set_stars(latest_tsqmi.value)

        svg_data = open(f'/src/tsqmi/media/{result}stars.svg', "rb").read()
        return HttpResponse(svg_data, content_type="image/svg+xml")


class CalculatedTSQMIHistoryModelViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    ViewSet para cadastrar as medidas coletadas
    """

    serializer_class = TSQMISerializer

    def get_repository(self):
        return get_object_or_404(
            Repository,
            id=self.kwargs['repository_pk'],
            product_id=self.kwargs['product_pk'],
            product__organization_id=self.kwargs['organization_pk'],
        )

    def get_queryset(self):
        repository = get_object_or_404(
            Repository,
            id=self.kwargs['repository_pk'],
            product_id=self.kwargs['product_pk'],
            product__organization_id=self.kwargs['organization_pk'],
        )
        return repository.calculated_tsqmis.all().reverse()


class CalculateTSQMI(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = TSQMISerializer

    def get_repository(self):
        return get_object_or_404(
            Repository,
            id=self.kwargs['repository_pk'],
            product_id=self.kwargs['product_pk'],
            product__organization_id=self.kwargs['organization_pk'],
        )

    def get_product(self):
        return get_object_or_404(
            Product,
            id=self.kwargs['product_pk'],
            organization_id=self.kwargs['organization_pk'],
        )

    def create(self, request, *args, **kwargs):
        serializer = TSQMICalculationRequestSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        created_at = serializer.validated_data['created_at']

        repository: Repository = self.get_repository()
        pre_config = repository.product.release_configuration.first()

        product = self.get_product()
        pre_config = product.release_configuration.first()

        # 2. Get queryset
        # TODO: Gambiarra, modelar model para nível acima
        characteristics_keys = [
            characteristic['key']
            for characteristic in pre_config.data['characteristics']
        ]
        qs = (
            SupportedCharacteristic.objects.filter(
                key__in=characteristics_keys
            )
            .prefetch_related('calculated_characteristics')
            .first()
        )

        chars_params = []
        try:
            chars_params = qs.get_latest_characteristics_params(
                pre_config,
            )
        except CharacteristicNotDefinedInReleaseConfigurationuration as exc:
            return Response(
                {'error': str(exc)},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
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
            repository=repository,
            value=data['value'],
            created_at=created_at,
        )

        serializer = TSQMISerializer(tsqmi)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
