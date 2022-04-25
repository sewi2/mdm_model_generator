from typing import Union

from openapi_model_generator.generators.base_filters import (
    to_field_name,
)
from openapi_model_generator.generators.models.fields import ModelFieldGenerator
from openapi_model_generator.renderer import TemplateRenderer


class ModelGenerator:
    TEMPLATE_NAME = 'base_models'
    FILTERS = {
        'to_model_field': ModelFieldGenerator(),
        'to_field_name': to_field_name,
    }

    def __init__(self):
        self._template_renderer = TemplateRenderer(self.TEMPLATE_NAME, self.FILTERS)

    def generate(self, schema: Union[str, dict]):  # noqa: pylint=arguments-differ
        return self._template_renderer.render(schema)
