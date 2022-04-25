from typing import Union

from openapi_model_generator.generators.base_filters import (
    to_field_name,
)
from openapi_model_generator.renderer import TemplateRenderer
from openapi_model_generator.generators.serializers.fields import SerializerFieldGenerator
from openapi_model_generator.generators.serializers.filters import get_serializer_fields


class SerializerGenerator:
    TEMPLATE_NAME = 'base_serializers'
    FILTERS = {
        'to_serializer_field': SerializerFieldGenerator(),
        'to_field_name': to_field_name,
        'get_serializer_fields': get_serializer_fields,
    }

    def __init__(self):
        self._template_renderer = TemplateRenderer(self.TEMPLATE_NAME, self.FILTERS)

    def generate(self, schema: Union[str, dict]):  # noqa: pylint=arguments-differ
        return self._template_renderer.render(schema)
