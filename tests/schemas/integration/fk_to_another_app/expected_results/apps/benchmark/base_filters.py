from rest_framework_filters import AutoFilter
from pik.api.filters import StandardizedFilterSet

from . import base_models as base_module


class BaseBenchmarkCatalogObjectHeaderFilter(StandardizedFilterSet):
    uid = AutoFilter(lookups=['exact', 'gt', 'gte', 'lt', 'lte', 'in', 'isnull'])
    created = AutoFilter(lookups=['exact', 'gt', 'gte', 'lt', 'lte', 'in', 'isnull'])
    updated = AutoFilter(lookups=['exact', 'gt', 'gte', 'lt', 'lte', 'in', 'isnull'])
    deleted = AutoFilter(lookups=['exact', 'gt', 'gte', 'lt', 'lte', 'in', 'isnull'])
    valid_object_guid = AutoFilter(lookups=['exact', 'gt', 'gte', 'lt', 'lte', 'in', 'isnull'])
    valid_object_type = AutoFilter(lookups=['exact', 'iexact', 'in', 'startswith', 'endswith', 'contains', 'isnull'])
    string_field = AutoFilter(lookups=['exact', 'iexact', 'in', 'startswith', 'endswith', 'contains', 'isnull'])
    string_uuid = AutoFilter(lookups=['exact', 'gt', 'gte', 'lt', 'lte', 'in', 'isnull'])
    string_date_time = AutoFilter(lookups=['exact', 'gt', 'gte', 'lt', 'lte', 'in', 'isnull'])
    string_date = AutoFilter(lookups=['exact', 'gt', 'gte', 'lt', 'lte', 'in', 'isnull'])
    number_field = AutoFilter(lookups=['exact', 'gt', 'gte', 'lt', 'lte', 'in', 'isnull'])
    decimal_field = AutoFilter(lookups=['exact', 'gt', 'gte', 'lt', 'lte', 'in', 'isnull'])
    integer_field = AutoFilter(lookups=['exact', 'gt', 'gte', 'lt', 'lte', 'in', 'isnull'])
    is_boolean = AutoFilter(lookups=['exact', 'in', 'isnull'])
    enum_string = AutoFilter(lookups=['exact', 'iexact', 'in', 'startswith', 'endswith', 'contains', 'isnull'])
    enum_integer = AutoFilter(lookups=['exact', 'gt', 'gte', 'lt', 'lte', 'in', 'isnull'])
    hash = AutoFilter(lookups=['exact', 'iexact', 'in', 'startswith', 'endswith', 'contains', 'isnull'])
    encrypted = AutoFilter(lookups=['exact', 'iexact', 'in', 'startswith', 'endswith', 'contains', 'isnull'])
    comment = AutoFilter(lookups=['exact', 'iexact', 'in', 'startswith', 'endswith', 'contains', 'isnull'])

    class Meta:
        fields = ()
