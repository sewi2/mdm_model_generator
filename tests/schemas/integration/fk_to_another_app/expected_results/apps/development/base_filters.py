from rest_framework_filters import AutoFilter
from pik.api.filters import StandardizedFilterSet

from . import base_models as base_module


class BaseDevelopmentCatalogObjectTableFilter(StandardizedFilterSet):
    uid = AutoFilter(lookups=['exact', 'gt', 'gte', 'lt', 'lte', 'in', 'isnull'])
    created = AutoFilter(lookups=['exact', 'gt', 'gte', 'lt', 'lte', 'in', 'isnull'])
    updated = AutoFilter(lookups=['exact', 'gt', 'gte', 'lt', 'lte', 'in', 'isnull'])
    deleted = AutoFilter(lookups=['exact', 'gt', 'gte', 'lt', 'lte', 'in', 'isnull'])
    valid_object_guid = AutoFilter(lookups=['exact', 'gt', 'gte', 'lt', 'lte', 'in', 'isnull'])
    valid_object_type = AutoFilter(lookups=['exact', 'iexact', 'in', 'startswith', 'endswith', 'contains', 'isnull'])
    line_number = AutoFilter(lookups=['exact', 'gt', 'gte', 'lt', 'lte', 'in', 'isnull'])
    string_field = AutoFilter(lookups=['exact', 'iexact', 'in', 'startswith', 'endswith', 'contains', 'isnull'])
    string_date_time = AutoFilter(lookups=['exact', 'gt', 'gte', 'lt', 'lte', 'in', 'isnull'])

    class Meta:
        fields = ()
