import inspect
import os
import re
from os.path import exists

from djangorestframework_camel_case.util import camel_to_underscore


def to_model_field_name(name: str) -> str:
    """
    Cleanups field name.

    Replaces `-` to '_' and `guid` to `uid` in field names.
    Cleanups leading underscores (_).
    Makes CamelCase as an under_score one.
    """

    name = name.lstrip('_').replace('-', '_')
    if name == 'guid':
        name = 'uid'
    return camel_to_underscore(name)


def to_safe_string(value: str) -> str:
    """Converts string to an escaped one"""

    return repr(str(value))


def define_missing_classes(base_module, variables, base_class):
    def is_model(item):
        return (
                inspect.isclass(item)
                and item.__module__ == base_module.__name__
                and issubclass(item, base_class))

    for name, base in inspect.getmembers(base_module, is_model):
        match = re.match('Base(?P<name>.+)', name)
        if not match or match['name'] in variables:
            continue

        variables[match['name']] = type(
            match['name'], (base,), {'__module__': variables['__name__']})


def get_module_classes(module, predicate=None):
    return {
        name: item
        for name, item in inspect.getmembers(module, predicate)
        if item.__module__ == module.__name__
    }


def write_to_file(path, content):
    with open(path, 'w', encoding="utf-8") as file_obj:
        file_obj.write(content)


def write_if_not_exists(path, content, force=False):
    if exists(path) and not force:
        return
    write_to_file(path, content)


def create_directory(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


def get_serializer_fields(definition: dict):
    return [
        to_model_field_name(prop_name)
        for prop_name in
        list(definition.get("properties", {}).keys())
    ]
