# type: ignore
from decimal import Decimal
from typing import Optional, NoReturn

from mdm_model_generator.generators.base_filters import to_python_kwargs


class DecimalFieldMixin:

    DEFAULT_DECIMAL_FIELD_DECIMAL_PLACES = 2
    DEFAULT_DECIMAL_FIELD_MAX_DIGITS = 10

    @property
    def decimal_places(self) -> int:

        """
        Get places after dot `.` in DecimalField or default

        >>> decimal_mixin = DecimalFieldMixin()
        >>> decimal_mixin._schema = {'multipleOf': 0.1}
        >>> decimal_mixin.decimal_places
        1
        >>> decimal_mixin._schema = {'multipleOf': 0.01}
        >>> decimal_mixin.decimal_places
        2
        >>> decimal_mixin._schema = {'multipleOf': 0.001}
        >>> decimal_mixin.decimal_places
        3
        >>> decimal_mixin._schema = {'multipleOf': None}
        >>> decimal_mixin.decimal_places
        2
        >>> decimal_mixin._schema = {}
        >>> decimal_mixin.decimal_places
        2

        # Note: `0.99999999999999999999999999999999999` becomes 1.0
        >>> decimal_mixin._schema = {
        ... 'multipleOf': 0.99999999999999999999999999999999999}
        >>> decimal_mixin.decimal_places
        1

        # Note: Decimal('0.99999999999999999999999999999999999')
        # remains the same.
        >>> decimal_mixin._schema = {
        ... 'multipleOf': Decimal('0.99999999999999999999999999999999999')}
        >>> decimal_mixin.decimal_places
        35
        """

        return (
            -Decimal(str(self._schema['multipleOf']))
            .as_tuple().exponent
            if self._schema.get('multipleOf')
            else self.DEFAULT_DECIMAL_FIELD_DECIMAL_PLACES)

    def get_decimal_max_digits(self, decimal_places: int) -> int:

        """
        Get DecimalField `max_digits` parameters.
        Calcucated as `(maximum/minimum length
        of int part or default) + decimal_places`

        >>> decimal_mixin = DecimalFieldMixin()
        >>> decimal_mixin._schema = {'maximum': 10000}
        >>> decimal_mixin.get_decimal_max_digits(4)
        9
        >>> decimal_mixin._schema = {'maximum': 99999.999}
        >>> decimal_mixin.get_decimal_max_digits(3)
        8
        >>> decimal_mixin._schema = {'minimum': 10000}
        >>> decimal_mixin.get_decimal_max_digits(4)
        9
        >>> decimal_mixin._schema = {
        ... 'minimum': -99999.999, 'maximum': 99999.999}
        >>> decimal_mixin.get_decimal_max_digits(3)
        8
        >>> decimal_mixin._schema = {
        ... 'minimum': -99999.999, 'maximum': 999.999}
        >>> decimal_mixin.get_decimal_max_digits(4)
        9
        >>> decimal_mixin._schema = {'maximum': 99999.999}
        >>> decimal_mixin.get_decimal_max_digits(3)
        8
        >>> decimal_mixin._schema = {'maximum': None}
        >>> decimal_mixin.get_decimal_max_digits(3)
        13
        >>> decimal_mixin._schema = {'minimum': None}
        >>> decimal_mixin.get_decimal_max_digits(3)
        13
        >>> decimal_mixin._schema = {'minimum': None, 'maximum': None}
        >>> decimal_mixin.get_decimal_max_digits(5)
        15

        # Float `-9999999999999.9999999999` becomes `-10000000000000.0`
        # (python adds 1 extra symbol into the lenght, if not using Decimal)
        >>> decimal_mixin._schema = {
        ... "minimum": -9999999999999.9999999999,
        ... "maximum": 9999999999999.9999999999,
        ... "multipleOf": 0.0000000001}
        >>> decimal_mixin.get_decimal_max_digits(10)
        24

        # The same float length as in the previous test,
        # despite a different "visual" length.
        >>> decimal_mixin._schema = {
        ... "minimum": -10000000000000,
        ... "maximum": 10000000000000,
        ... "multipleOf": 0.0000000001}
        >>> decimal_mixin.get_decimal_max_digits(10)
        24

        # Hovewer, DecimalField works correctly.
        >>> decimal_mixin._schema = {
        ... "minimum": Decimal('-9999999999999.9999999999'),
        ... "maximum": Decimal('9999999999999.9999999999'),
        ... "multipleOf": 0.0000000001}
        >>> decimal_mixin.get_decimal_max_digits(10)
        23
        >>> decimal_mixin._schema = {
        ... "minimum": Decimal('-10000000000000'),
        ... "maximum": Decimal('10000000000000'),
        ... "multipleOf": 0.0000000001}
        >>> decimal_mixin.get_decimal_max_digits(10)
        24

        # See the difference (the same numbers becomes as different lenghts):
        >>> decimal_mixin._schema = {
        ... 'minimum': Decimal('-9999999999999999.999999999999'),
        ... 'maximum': Decimal('99999999999999.999999999999')}
        >>> decimal_mixin.get_decimal_max_digits(4)
        20
        >>> decimal_mixin._schema = {
        ... 'minimum': -9999999999999999.999999999999,
        ... 'maximum': 99999999999999.999999999999}
        >>> decimal_mixin.get_decimal_max_digits(4)
        21
        """

        minimum, maximum = ('minimum', 'maximum')
        _min = Decimal(str(int(self._schema.get(minimum) or 0))).as_tuple()
        _max = Decimal(str(int(self._schema.get(maximum) or 0))).as_tuple()
        _max_int_digits = max(len(_min.digits), len(_max.digits))
        return (
            _max_int_digits + decimal_places
            if _max_int_digits != 1
            else (self.DEFAULT_DECIMAL_FIELD_MAX_DIGITS
                  + decimal_places))


class CommonFieldGeneratorMixin:  # noqa: pylint - too-many-public-methods
    SCHEMA_FK_FIELDS = ('oneOf', 'anyOf', 'allOf')

    # Schema and django generator field type mapping.
    SCHEMA_BOOLEAN_TYPE = 'boolean'
    SCHEMA_DECIMAL_TYPE = 'number'
    SCHEMA_INTEGER_TYPE = 'integer'
    SCHEMA_STRING_TYPE = 'string'

    # Default values.
    DEFAULT_CHAR_MAX_LENGTH = 255

    IS_FORCE_BLANK_ENABLED = True
    IS_FORCE_NULL_ENABLED = True

    @property
    def definition(self) -> str:
        kwargs = to_python_kwargs(self.kwargs)
        return f"{self.type}({kwargs})"

    @property
    def kwargs(self) -> dict:
        return self.clean_kwargs

    @property
    def clean_kwargs(self) -> dict:
        return NotImplementedError  # noqa: Expected type dict

    @property
    def no_clean_kwargs(self) -> dict:
        return NotImplementedError  # noqa: Expected type dict

    @property
    def default_kwargs(self) -> dict:
        return NotImplementedError  # noqa: Expected type dict

    @property
    def guid_kwargs(self) -> dict:
        return {**self.DEFAULT_UUID_KWARGS} if self._name == 'guid' else {}

    @property
    def choices_kwargs(self) -> dict:
        return NotImplementedError  # noqa: Expected type dict

    @property
    def type_kwargs(self) -> dict:
        return NotImplementedError  # noqa: Expected type dict

    @property
    def optional_kwargs(self) -> dict:
        return NotImplementedError  # noqa: Expected type dict

    @property
    def type(self) -> str:
        """Returns django field name according the schema key"""

        return NotImplementedError  # noqa: Expected type dict

    def clean_extra_guid_kwargs(self, kwargs: dict) -> NoReturn:
        if self._name == 'guid':
            for key in self.UUID_NOT_USED_PARAMS:
                if key in kwargs:
                    del kwargs[key]
        return kwargs

    @property
    def has_object_enums(self) -> bool:
        return self.is_object and self.fk_model_name

    @property
    def is_object(self) -> bool:
        return self.schema_type == "object"

    @property
    def fk_model_name(self) -> Optional[str]:
        enum = (
            self._schema.get('properties', {}).get('type', {}).get('enum', []))
        return enum[0] if enum else None

    @property
    def field_type_mapping(self) -> dict:
        return {
            self.SCHEMA_STRING_TYPE: self.field_type_from_format,
            self.SCHEMA_INTEGER_TYPE: self.INTEGER,
            self.SCHEMA_BOOLEAN_TYPE: self.BOOLEAN,
            self.SCHEMA_DECIMAL_TYPE: self.DECIMAL}

    @property
    def field_type_from_format(self) -> str:
        """
        Get django field type
        according to a schema string field format
        """

        return self.STRING_FORMAT_TO_FIELD_NAME.get(
            self.field_format, self.CHAR)

    @property
    def field_format(self) -> str:
        return self._schema.get('format')

    @property
    def is_required(self) -> bool:
        return self._name in self._required_fields

    @property
    def is_nullable(self) -> bool:
        return self._schema.get('nullable', False)

    @property
    def schema_type(self) -> str:
        return self._schema.get('type')

    @property
    def schema_enum(self) -> Optional[list]:
        return self._schema.get('enum')

    @property
    def title(self) -> str:
        return f"_({repr(self._schema.get('title', ''))})"

    @property
    def description(self) -> str:
        return f"_({repr(self._schema.get('description', ''))})"

    @property
    def is_force_blank_enabled(self) -> bool:
        return self.IS_FORCE_BLANK_ENABLED

    @property
    def is_force_null_enabled(self) -> bool:
        return self.IS_FORCE_NULL_ENABLED

    @property
    def is_blank_kwarg(self) -> bool:
        return self.is_required or self.is_force_blank_enabled

    @property
    def is_null_kwarg(self) -> bool:
        return self.is_nullable or self.is_force_null_enabled
