from typing import List

from mdm_model_generator.generators.base_filters import to_field_name
from mdm_model_generator.generators.mixins import (  # type: ignore
    DecimalFieldMixin, CommonFieldGeneratorMixin)
from mdm_model_generator.generators.models.fields import ModelChoicesGenerator


class SerializerFieldGenerator(DecimalFieldMixin, CommonFieldGeneratorMixin):
    # Default django serializer field names.
    BOOLEAN = 'serializers.BooleanField'
    CHAR = 'serializers.CharField'
    CHOICES = 'serializers.ChoiceField'
    DATETIME = 'serializers.DateTimeField'
    DATE = 'serializers.DateField'
    DECIMAL = 'serializers.DecimalField'
    EMAIL = 'serializers.EmailField'
    FOREIGN_KEY = 'LazyField'
    INTEGER = 'serializers.IntegerField'
    JSON = 'serializers.JSONField'
    UUID = 'serializers.UUIDField'

    # Additional options.
    DEFAULT_FIELD = JSON

    # Schema and django serializer strings` field name mapping.
    STRING_FORMAT_TO_FIELD_NAME = {
        'date': DATE,
        'date-time': DATETIME,
        'email': EMAIL,
        'uuid': UUID,
    }

    EXCLUDED_FIELD_NAMES: list = []
    UUID_NOT_USED_PARAMS = ('allow_null', 'allow_blank', )
    DEFAULT_UUID_KWARGS = {'read_only': True}

    def __call__(
            self, schema: dict, name: str,
            serializer_name: str, required_fields: List[str]) -> str:

        self._schema = schema
        self._name = name
        self._serializer_name = serializer_name
        self._required_fields = required_fields

        return self.definition  # type: ignore

    @property
    def clean_kwargs(self) -> dict:
        return self._clean_none_kwargs(
            self.clean_extra_guid_kwargs(self.no_clean_kwargs))

    @property
    def no_clean_kwargs(self) -> dict:
        return {
            **self.default_kwargs,
            **self.guid_kwargs,
            **self.type_kwargs}

    @property
    def default_kwargs(self) -> dict:
        return {
            'label': self.title,
            'help_text': self.description,
            **self.optional_kwargs}

    @property
    def type(self) -> str:
        if self.has_object_enums:
            field_type = self.FOREIGN_KEY
        elif self.schema_enum:
            field_type = self.CHOICES
        else:
            field_type = self.field_type_mapping.get(
                self.schema_type, self.DEFAULT_FIELD)
        return field_type

    @property
    def optional_kwargs(self) -> dict:
        return {
            'allow_blank': self.is_blank_kwarg,
            'allow_null': self.is_null_kwarg}

    @property
    def _field_type_kwargs_mapping(self) -> dict:
        return {
            self.DECIMAL: {
                'max_digits': self.get_decimal_max_digits(
                    self.decimal_places),
                'decimal_places': self.decimal_places,
                'min_value': self._schema.get('minimum'),
                'max_value': self._schema.get('maximum'),
                'allow_blank': None,
            },
            self.BOOLEAN: {
                'allow_blank': None,
            },
            self.INTEGER: {
                'min_value': self._schema.get('minimum'),
                'max_value': self._schema.get('maximum'),
                'allow_blank': None,
            },
            self.UUID: {
                'allow_blank': None,
            },
            self.CHAR: {
                'max_length': self._schema.get(
                    'maxLength', self.DEFAULT_CHAR_MAX_LENGTH),
            },
            **{_format: {'allow_blank': None}
               for _format in self.STRING_FORMAT_TO_FIELD_NAME.values()},
            self.FOREIGN_KEY: {
                'allow_blank': None,
                'path': repr(f'Base{self.fk_model_name}Serializer'),
            },
            self.JSON: {
                **self._jsonfield_help_text_kwargs,
                'default': 'dict',
                'allow_blank': None,
            },
            self.CHOICES: {
                **self.choices_kwargs,
            },
        }

    @property
    def type_kwargs(self) -> dict:
        return (  # type: ignore
            self._field_type_kwargs_mapping.get(
                self.type, {}))

    @property
    def choices_kwargs(self) -> dict:
        kwargs = {}
        if self.schema_enum:
            choices_name = ModelChoicesGenerator.get_choices_name(
                to_field_name(self._name))
            kwargs['choices'] = (
                f"base_models.Base{self._serializer_name}.{choices_name}")
        return kwargs

    @property
    def _jsonfield_help_text_kwargs(self) -> dict:
        items_help_text = self._schema.get('items', {}).get('title')
        return {
            'help_text': repr(items_help_text)
            if items_help_text
            else self.description}

    @staticmethod
    def _clean_none_kwargs(kwargs: dict) -> dict:
        for key, value in kwargs.copy().items():
            if kwargs[key] is None:
                del kwargs[key]
        return kwargs
