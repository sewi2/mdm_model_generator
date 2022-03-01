from typing import Optional

import jinja2
from prance import ResolvingParser
from prance.util.resolver import (
    RESOLVE_FILES, RESOLVE_HTTP,
)

from .model_field_generator import ModelFieldGenerator
from .serializer_field_generator import SerializerFieldGenerator
from .utils import (
    to_model_field_name,
    to_safe_string, get_serializer_fields,
)


class Generator:
    MAJOR_VERSION = 0

    def __init__(self, templates, schema):
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(templates),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.parser = ResolvingParser(
            spec_string=schema, backend='openapi-spec-validator', strict=False,
            resolve_types=RESOLVE_HTTP | RESOLVE_FILES,
        )
        self.env.filters.update({
            'to_model_field': ModelFieldGenerator(),
            'to_model_field_name': to_model_field_name,
            'to_serializer_field': SerializerFieldGenerator(),
            'to_serializer_field_name': to_model_field_name,
            'get_serializer_fields': get_serializer_fields,
            'to_safe_string': to_safe_string,
        })

    def get_version(self) -> str:
        return self.parser.version_parsed[self.MAJOR_VERSION]

    def get_v2_definitions(self) -> dict:
        return self.parser.specification['definitions']

    def get_v3_definitions(self) -> dict:
        return self.parser.specification['components']['schemas']

    def get_definitions(self) -> Optional[dict]:
        version = self.get_version()
        if version == 2:
            return self.get_v2_definitions()
        if version == 3:
            return self.get_v3_definitions()
        raise Exception(f'Unknown schema version - {self.parser.version}')

    def generate(self, name) -> str:
        """Generates model or serializer file according to a given jinja template name"""

        return self.env.get_template(name + '.j2py').render({
            'definitions': self.get_definitions(),
        })
