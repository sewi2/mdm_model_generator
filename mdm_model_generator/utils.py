import os
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
