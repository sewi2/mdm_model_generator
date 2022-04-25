from djangorestframework_camel_case.util import camel_to_underscore


def to_field_name(name: str) -> str:
    """
    Cleanups field name.

    Replaces `-` to '_' and `guid` to `uid` in field names.
    Makes CamelCase as an under_score one.
    """

    if name == 'guid':
        name = 'uid'
    return camel_to_underscore(name)
