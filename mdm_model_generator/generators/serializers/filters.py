from typing import List

from mdm_model_generator.generators.base_filters import to_field_name
from mdm_model_generator.generators.serializers.fields import (
    SerializerFieldGenerator)


def get_serializer_fields(definition: dict) -> List[str]:
    return [
        prop_name if prop_name == 'guid' else to_field_name(prop_name)
        for prop_name in
        [
            field_name for field_name
            in definition.get("properties", {}).keys()
            if field_name not in SerializerFieldGenerator.EXCLUDED_FIELD_NAMES
        ]
    ]
