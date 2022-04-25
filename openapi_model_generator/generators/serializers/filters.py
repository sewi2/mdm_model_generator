from typing import List

from openapi_model_generator.generators.base_filters import to_field_name
from openapi_model_generator.generators.serializers.fields import SerializerFieldGenerator


def get_serializer_fields(definition: dict) -> List[str]:
    return [
        to_field_name(prop_name)
        for prop_name in
        [
            field_name for field_name in definition.get("properties", {}).keys()
            if field_name not in SerializerFieldGenerator.EXCLUDED_FIELD_NAMES
        ]
    ]
