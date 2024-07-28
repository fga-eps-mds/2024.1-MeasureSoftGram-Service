"""
Views que realiza a coleta de métricas no repositório github
"""

import concurrent.futures

from django.conf import settings
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from collectors.github import utils
from collectors.github.serializers import GithubCollectorParamsSerializer
from metrics.serializers import LatestCollectedMetricSerializer
from organizations.models import Repository
from metrics.models import CollectedMetric, SupportedMetric
from metrics.serializers import CollectedMetricSerializer
from utils import namefy


def import_github_metrics(data, repository):
    supported_metrics = {
        supported_metric.key: supported_metric
        for supported_metric in SupportedMetric.objects.all()
    }

    collected_metrics = []

    for metric in data["metrics"]:
        metric_key = metric["name"]
        metric_value = metric["value"]

        if metric_key not in supported_metrics:
            return

        obj = {
            "path": metric["path"],
            "metric": supported_metrics[metric_key],
            "value": float(metric_value),
        }

        in_memory_metric = CollectedMetric(**obj)
        collected_metrics.append(in_memory_metric)

    for collected_metric in collected_metrics:
        collected_metric.repository = repository

    saved_metrics = CollectedMetric.objects.bulk_create(collected_metrics)

    return CollectedMetricSerializer(saved_metrics, many=True).data


class ImportGithubMetricsViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = GithubCollectorParamsSerializer
    queryset = SupportedMetric.objects.all()

    def get_repository(self):
        return get_object_or_404(
            Repository,
            id=self.kwargs["repository_pk"],
            product_id=self.kwargs["product_pk"],
            product__organization_id=self.kwargs["organization_pk"],
        )

    def create(self, request, *args, **kwargs):
        # TODO VALIDACAO COM O SERIALIZER
        data = dict(request.data)
        repository = self.get_repository()
        json_data = import_github_metrics(data, repository)
        return Response(json_data)
