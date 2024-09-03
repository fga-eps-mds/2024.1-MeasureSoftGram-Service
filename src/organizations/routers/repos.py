from characteristics.views import (
    CalculateCharacteristicViewSet,
    CalculatedCharacteristicHistoryModelViewSet,
    LatestCalculatedCharacteristicModelViewSet,
)
from collectors.github.view import ImportGithubMetricsViewSet
from collectors.sonarqube.view import ImportSonarQubeMetricsViewSet
from math_model.views import CalculateMathModelViewSet
from measures.views import (
    CalculatedMeasureHistoryModelViewSet,
    CalculateMeasuresViewSet,
    LatestCalculatedMeasureModelViewSet,
)
from metrics.views import (
    CollectedMetricHistoryModelViewSet,
    CollectedMetricModelViewSet,
    LatestCollectedMetricModelViewSet,
)
from organizations.routers.routers import Router
from subcharacteristics.views import (
    CalculatedSubCharacteristicHistoryModelViewSet,
    CalculateSubCharacteristicViewSet,
    LatestCalculatedSubCharacteristicModelViewSet,
)
from tsqmi.views import (
    CalculatedTSQMIHistoryModelViewSet,
    CalculateTSQMI,
    LatestCalculatedTSQMIBadgeViewSet,
    LatestCalculatedTSQMIViewSet,
)


class RepoRouter(Router):
    def __init__(self, parent_router, **children):
        super().__init__(
            parent_router,
            'repositories',
            'repository',
            children=[
                *self._get_actions_endpoints_dicts(),
                *self._get_latest_values_endpoints_dict(),
                *self._get_historic_values_endpoints_dicts(),
                *self._get_collectors_endpoints_dict(),
                *children,
            ],
        )

    def _get_actions_endpoints_dicts(self):
        return [
            {
                'name': 'collect/metrics',
                'view': CollectedMetricModelViewSet,
                'basename': '',
            },
            {
                'name': 'calculate/measures',
                'view': CalculateMeasuresViewSet,
                'basename': 'calculate-measures',
            },
            {
                'name': 'calculate/subcharacteristics',
                'view': CalculateSubCharacteristicViewSet,
                'basename': 'calculate-subcharacteristics',
            },
            {
                'name': 'calculate/characteristics',
                'view': CalculateCharacteristicViewSet,
                'basename': 'calculate-characteristics',
            },
            {
                'name': 'calculate/tsqmi',
                'view': CalculateTSQMI,
                'basename': 'calculate-tsqmi',
            },
        ]

    def _get_latest_values_endpoints_dict(self):
        return [
            {
                'name': 'latest-values/metrics',
                'view': LatestCollectedMetricModelViewSet,
                'basename': 'latest-collected-metrics',
            },
            {
                'name': 'latest-values/measures',
                'view': LatestCalculatedMeasureModelViewSet,
                'basename': 'latest-calculated-measures',
            },
            {
                'name': 'latest-values/subcharacteristics',
                'view': LatestCalculatedSubCharacteristicModelViewSet,
                'basename': 'latest-calculated-subcharacteristics',
            },
            {
                'name': 'latest-values/characteristics',
                'view': LatestCalculatedCharacteristicModelViewSet,
                'basename': 'latest-calculated-characteristics',
            },
            {
                'name': 'latest-values/tsqmi',
                'view': LatestCalculatedTSQMIViewSet,
                'basename': 'latest-calculated-tsqmi',
            },
            {
                "name": "latest-values/tsqmi/badge",
                "view": LatestCalculatedTSQMIBadgeViewSet,
                "basename": "latest-calculated-tsqmi-badge",
            },
        ]

    def _get_historic_values_endpoints_dicts(self):
        return [
            {
                'name': 'historical-values/metrics',
                'view': CollectedMetricHistoryModelViewSet,
                'basename': 'metrics-historical-values',
            },
            {
                'name': 'historical-values/measures',
                'view': CalculatedMeasureHistoryModelViewSet,
                'basename': 'measures-historical-values',
            },
            {
                'name': 'historical-values/subcharacteristics',
                'view': CalculatedSubCharacteristicHistoryModelViewSet,
                'basename': 'subcharacteristics-historical-values',
            },
            {
                'name': 'historical-values/characteristics',
                'view': CalculatedCharacteristicHistoryModelViewSet,
                'basename': 'characteristics-historical-values',
            },
            {
                'name': 'historical-values/tsqmi',
                'view': CalculatedTSQMIHistoryModelViewSet,
                'basename': 'tsqmi-historical-values',
            },
        ]

    def _get_collectors_endpoints_dict(self):
        return [
            # {
            #     'name': 'collectors/github',
            #     'view': ImportGithubMetricsViewSet,
            #     'basename': 'github-collector',
            # },
            # {
            #     'name': 'collectors/sonarqube',
            #     'view': ImportSonarQubeMetricsViewSet,
            #     'basename': 'sonarqube-collector',
            # },
            {
                'name': 'calculate/math-model', 
                'view': CalculateMathModelViewSet, 
                'basename': 'calculate-math-model'
            }
        ]
