from typing import Any, Iterable

from pik.utils.case_utils import camel_to_underscore  # type: ignore


def to_field_name(name: str) -> str:
    """
    Cleanups field name.
    Replaces `-` to '_' and `guid` to `uid` in field names.
    Makes CamelCase as an under_score one.

    >>> to_field_name('uid')
    'uid'
    >>> to_field_name('guid')
    'uid'
    >>> to_field_name('camelCaseField')
    'camel_case_field'
    >>> to_field_name('CamelCaseField')
    'camel_case_field'
    >>> to_field_name('camelCasefield')
    'camel_casefield'
    >>> to_field_name('CamelCasefield')
    'camel_casefield'
    >>> to_field_name('Camelcasefield')
    'camelcasefield'
    >>> to_field_name('Camel-case-field')
    'camel_case_field'
    >>> to_field_name('camel-case-field')
    'camel_case_field'
    """

    if name == 'guid':
        name = 'uid'
    return camel_to_underscore(name)  # type: ignore


def to_python_kwargs(val: dict) -> str:
    """
    Returns string formatted as
    'param1=val1, param2=val2, ...' from dict.

    >>> to_python_kwargs({'foo': 1})
    'foo=1'
    >>> to_python_kwargs({'foo': 1, 'b': 'xx'})
    'foo=1, b=xx'
    >>> to_python_kwargs({})
    ''
    """

    return ', '.join([f"{k}={v}" for k, v in val.items()])


def str_to_python(item: Any) -> Any:
    """
    Converts a string to a python object.

    >>> str_to_python('true')
    True
    >>> str_to_python('false')
    False
    >>> str_to_python('none')

    >>> str_to_python('123')
    '123'
    >>> str_to_python(123)
    123
    """

    mapping = {
        'true': True,
        'false': False,
        'none': None}

    if isinstance(item, str) and item.lower() in mapping:
        return mapping.get(item.lower())

    return item


def convert_strings_to_python_objects(iterable: Iterable) -> list:
    """
    Returns list of values
    returned by `str_to_python()` function.

    >>> convert_strings_to_python_objects(
    ... ['True','true','TRUE','TrUe', True])
    [True, True, True, True, True]

    >>> convert_strings_to_python_objects(
    ... ['False', 'false', 'FALSE', 'FaLse', False])
    [False, False, False, False, False]

    >>> convert_strings_to_python_objects(
    ... ['None', 'none', 'NONE', 'NoNe', None])
    [None, None, None, None, None]

    >>> convert_strings_to_python_objects(
    ... [123, '123', 123.45, {}, []])
    [123, '123', 123.45, {}, []]
    """

    return list(map(str_to_python, iterable))
