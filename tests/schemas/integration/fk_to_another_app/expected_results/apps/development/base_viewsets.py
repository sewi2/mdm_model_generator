from pik.api.viewsets import RestQLStandardizedModelViewSet

from . import base_serializers
from . import base_filters


class BaseDevelopmentCatalogObjectTableViewSet(RestQLStandardizedModelViewSet):

    lookup_field = 'uid'
    lookup_url_kwarg = 'guid'
    ordering = '-created'
    serializer_class = base_serializers.BaseDevelopmentCatalogObjectTableSerializer
    filterset_class = base_filters.BaseDevelopmentCatalogObjectTableFilter
    allow_history = False
    prefetch_related = {
        'header': (
            'header'),
    }

    search_fields = (
        'valid_object_type',
        'string_field',
    )
    ordering_fields = (
        'uid',
        'created',
        'updated',
        'deleted',
        'valid_object_type',
        'line_number',
        'string_field',
        'string_date_time',
    )
    default_restql_query = {'include': [
        '*',
        {'header': {
            'include': ['guid', 'type'], 'exclude': [],
            'arguments': {}, 'aliases': {}}},
    ], 'exclude': [], 'arguments': {}, 'aliases': {}}
