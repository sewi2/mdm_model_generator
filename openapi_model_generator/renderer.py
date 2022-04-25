from os.path import join, dirname
from typing import Union

import jinja2
from prance import ResolvingParser
from prance.util.resolver import (
    RESOLVE_FILES,
    RESOLVE_HTTP,
)


class TemplateRenderer:
    TEMPLATE_DIR = join(dirname(__file__), 'templates')

    def __init__(self, template_name: str, filters: dict):
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.TEMPLATE_DIR),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.env.filters.update(filters)
        self._template = self.env.get_template(template_name + '.j2py')

    def render(self, schema: Union[str, dict]) -> str:
        """Render template with schema supplied"""

        spec = ResolvingParser(
            spec_string=schema, backend='openapi-spec-validator', strict=False,
            resolve_types=RESOLVE_HTTP | RESOLVE_FILES,
        ).specification

        return self._template.render({
            'definitions': spec['components']['schemas'],
        })
