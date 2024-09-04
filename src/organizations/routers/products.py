from entity_trees.views import ReleaseConfigurationEntitiesRelationshipTreeViewSet
from goals.views import (
    CompareGoalsModelViewSet,
    CreateGoalModelViewSet,
    CurrentGoalModelViewSet,
    ReleaseListModelViewSet,
)
from organizations.routers.routers import Router
from organizations.views import (
    RepositoriesTSQMIHistoryViewSet,
    RepositoriesTSQMILatestValueViewSet,
    RepositoryViewSet,
)
from release_configuration.views import (
    CreateReleaseConfigurationModelViewSet,
    CurrentReleaseConfigurationModelViewSet,
)
from releases.views import CreateReleaseModelViewSet, ReleaseListAllModelViewSet


class ProductRouter(Router):
    def __init__(self, parent_router, **children):
        super().__init__(
            parent_router,
            'products',
            'product',
            children=[
                {
                    'name': 'entity-relationship-tree',
                    'view': ReleaseConfigurationEntitiesRelationshipTreeViewSet,
                    'basename': 'pre-config-entity-relationship-tree',
                },
                {
                    'name': 'repositories-tsqmi-latest-values',
                    'view': RepositoriesTSQMILatestValueViewSet,
                    'basename': 'repositories-tsqmi-latest-values',
                },
                {
                    'name': 'repositories-tsqmi-historical-values',
                    'view': RepositoriesTSQMIHistoryViewSet,
                    'basename': 'repositories-tsqmi-historical-values',
                },
                {
                    'name': 'repositories',
                    'view': RepositoryViewSet,
                    'basename': '',
                },
                *self._get_goals_endpoints_dicts(),
                *self._get_ReleaseConfigurations_endpoints_dict(),
                *children,
            ],
        )

    def _get_goals_endpoints_dicts(self):
        return [
            {
                'name': 'current/goal',
                'view': CurrentGoalModelViewSet,
                'basename': 'current-goal',
            },
            {
                'name': 'create/goal',
                'view': CreateGoalModelViewSet,
                'basename': 'create-goal',
            },
            {
                'name': 'all/goal',
                'view': CompareGoalsModelViewSet,
                'basename': 'all-goal',
            },
            {
                'name': 'release',
                'view': ReleaseListModelViewSet,
                'basename': 'release-list',
            },
            {
                'name': 'release/all',
                'view': ReleaseListAllModelViewSet,
                'basename': 'release-list-all',
            },
            {
                'name': 'create/release',
                'view': CreateReleaseModelViewSet,
                'basename': 'create-release',
            },
        ]

    def _get_ReleaseConfigurations_endpoints_dict(self):
        return [
            {
                'name': 'current/pre-config',
                'view': CurrentReleaseConfigurationModelViewSet,
                'basename': 'current-pre-config',
            },
            {
                'name': 'create/pre-config',
                'view': CreateReleaseConfigurationModelViewSet,
                'basename': 'create-pre-config',
            },
        ]
