from pik.api.viewsets import RestQLStandardizedModelViewSet

from . import base_serializers
from . import base_filters


class BaseBenchmarkCatalogObjectHeaderViewSet(RestQLStandardizedModelViewSet):

    lookup_field = 'uid'
    lookup_url_kwarg = 'guid'
    ordering = '-created'
    serializer_class = base_serializers.BaseBenchmarkCatalogObjectHeaderSerializer
    filterset_class = base_filters.BaseBenchmarkCatalogObjectHeaderFilter
    allow_history = False

    search_fields = (
        'valid_object_type',
        'string_field',
        'enum_string',
        'hash',
        'encrypted',
        'comment',
    )
    ordering_fields = (
        'uid',
        'created',
        'updated',
        'deleted',
        'valid_object_type',
        'string_field',
        'string_date_time',
        'string_date',
        'number_field',
        'decimal_field',
        'integer_field',
        'enum_string',
        'enum_integer',
        'hash',
        'encrypted',
        'comment',
    )
    default_restql_query = {'include': [
        '*',
    ], 'exclude': [], 'arguments': {}, 'aliases': {}}


class BaseBenchmarkCatalogObjectTableViewSet(RestQLStandardizedModelViewSet):

    lookup_field = 'uid'
    lookup_url_kwarg = 'guid'
    ordering = '-created'
    serializer_class = base_serializers.BaseBenchmarkCatalogObjectTableSerializer
    filterset_class = base_filters.BaseBenchmarkCatalogObjectTableFilter
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
