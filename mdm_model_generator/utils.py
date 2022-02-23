from typing import List

from djangorestframework_camel_case.util import camel_to_underscore


def to_model_field_name(name: str) -> str:
    """
    Cleanups field name.

    Replaces `-` to '_' and `guid` to `uid` in field names.
    Makes CamelCase as an under_score one.
    """

    if name == 'guid':
        name = 'uid'
    return camel_to_underscore(name)


def to_safe_string(value: str) -> str:
    """Converts string to an escaped one"""

    return repr(str(value))


def get_serializer_fields(definition: dict) -> List[str]:
    return [
        to_model_field_name(prop_name)
        for prop_name in
        list(definition.get("properties", {}).keys())
    ]
