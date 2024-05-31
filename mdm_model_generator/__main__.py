#!/usr/bin/env python

from __future__ import annotations

from itertools import chain

from argparse import ArgumentParser
from collections import Counter
from os.path import join, dirname
from pathlib import Path

import jinja2
import simplejson as json

from mdm_model_generator import __version__
from mdm_model_generator.generators.base_filters import (
    to_field_name,
)
from mdm_model_generator.generators.models.fields import (
    ModelFieldGenerator, ModelChoicesGenerator)
from mdm_model_generator.generators.serializers.fields import (
    SerializerFieldGenerator)
from mdm_model_generator.generators.serializers.filters import (
    get_serializer_fields)
from mdm_model_generator.generators.viewsets.filters import (
    is_fk_field,
    is_text_field,
    is_dated_string,
    is_number_field)


parser = ArgumentParser(
    prog=f"{__package__}",
    description='Generate models and serializers with '
                'OpenAPI flatten JSON-file (schema.esb.json)')
parser.add_argument(
    'schema',
    help="OpenAPI flatten JSON-file (schema.esb.json)")
parser.add_argument(
    'destination', default="../mdm_models/",
    help="Models and serializers destination directory")


args = parser.parse_args()


TEMPLATE_DIR = join(dirname(__file__), 'templates')

TEMPLATES = [
    '__init__.py',
    'base_models.py',
    'base_serializers.py',
    'base_filters.py',
    'base_viewsets.py',
    'apps/__init__.py',
    'apps/base_models.py',
    'apps/base_serializers.py',
    'apps/base_filters.py',
    'apps/base_viewsets.py',
]

FILTERS = {
    'to_model_field': ModelFieldGenerator(),
    'to_choices': ModelChoicesGenerator(),
    'to_serializer_field': SerializerFieldGenerator(),
    'to_field_name': to_field_name,
    'get_serializer_fields': get_serializer_fields,
    'is_fk_field': is_fk_field,
    'is_text_field': is_text_field,
    'is_dated_string': is_dated_string,
    'is_number_field': is_number_field,
}

MAX_RELATIONS_DEPTH = 10


def _write(template, template_name, context):
    content = template.render(context)
    with open(
            join(args.destination, template_name),
            'w', encoding='utf-8') as file_obj:
        file_obj.write(content)


def _get_app_definitions(context, tag_groups, app):
    return {
        schema: definition
        for schema, definition
        in context['definitions'].items()
        if schema in [
            group['tags'] for group in tag_groups
            if group['name'].lower() == app.lower()
        ][0]
    }


def _get_all_definitions(context):
    return {
        schema: definition
        for schema, definition
        in context['definitions'].items()
    }


def _get_app_models(definitions):
    return list(definitions.keys())


def _get_relations(model, definitions, visited_models=None):
    visited_models = visited_models or Counter({model: 1})
    fields = {}
    for prop_name, prop_definition in (
            definitions[model]['properties'].items()):
        if is_fk_field(prop_definition):
            fields[to_field_name(prop_name)] = to_field_name(prop_name)
            sub_model = (
                prop_definition
                .get('properties', {})
                .get('type', {})
                .get('enum', []))
            if not sub_model:
                continue
            sub_model = sub_model[0]
            if visited_models[sub_model] < MAX_RELATIONS_DEPTH:
                visited_models[sub_model] += 1
                sub_fields = _get_relations(
                    sub_model, definitions, visited_models)
                for subfield, relation in sub_fields.items():
                    fields[f'{to_field_name(prop_name)}.{subfield}'] = (
                        f'{to_field_name(prop_name)}__{relation}')
    return fields


def get_relations(app_definitions, all_definitions):
    return {
        model: _get_relations(model, all_definitions)
        for model in _get_app_models(app_definitions)
    }


def _write_to_apps(template, template_name, context, tag_groups: list[dict]):
    apps = [app['name'].lower() for app in tag_groups]
    for app in apps:
        destination = Path(args.destination) / 'apps' / app
        Path(destination).mkdir(
            parents=True, exist_ok=True)
        Path(Path(args.destination) / 'apps' / '__init__.py').touch(
            exist_ok=True)
        all_definitions = _get_all_definitions(context)
        app_definitions = _get_app_definitions(context, tag_groups, app)
        app_context = {
            **context,
            'definitions': app_definitions,
            'tag_groups': tag_groups,
            'relations': get_relations(app_definitions, all_definitions),
            'apps': apps,
            'app': app,
        }
        content = template.render(app_context)
        with open(join(destination, Path(template_name).name),
                  'w', encoding='utf-8') as file_obj:
            file_obj.write(content)


def main():
    with open(args.schema, encoding='utf-8') as file_obj:
        schema = json.load(file_obj, use_decimal=True)

    Path(args.destination).mkdir(parents=True, exist_ok=True)

    templates = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
        trim_blocks=True,
        lstrip_blocks=True)
    templates.filters.update(FILTERS)

    definitions = schema['components']['schemas']
    tag_groups = [
        {
            'name': tag_group['name'],
            'tags': tag_group['tags'],
        } for tag_group in schema["x-tagGroups"]
    ]
    tag_groups = [
        {
            'name': tag_name,
            'tags': list(chain(*[
                tag_group['tags']
                for tag_group in tag_groups if tag_group['name'] == tag_name]))
        } for tag_name in {tag_group['name'] for tag_group in tag_groups}
    ]

    apps = sorted([app['name'].lower() for app in tag_groups])

    context = {
        'version': f'{__version__}.{schema["info"]["version"][1:]}',
        'generator_version': f'{__version__}',
        'entities_version': f'{schema["info"]["version"][1:]}',
        'definitions': definitions,
        'apps': apps,
        'app': None,
    }

    for template_name in TEMPLATES:
        template = templates.get_template(
            f"{template_name.split('.py', maxsplit=1)[0]}.j2py")
        if 'apps/' in template_name:
            _write_to_apps(template, template_name, context, tag_groups)
        else:
            _write(template, template_name, context)


if __name__ == "__main__":
    main()
