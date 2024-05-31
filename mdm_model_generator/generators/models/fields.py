from __future__ import annotations

from typing import Optional, Tuple, List

from mdm_model_generator.generators.base_filters import (
    to_field_name, convert_strings_to_python_objects)
from mdm_model_generator.generators.mixins import (  # type: ignore
    DecimalFieldMixin, CommonFieldGeneratorMixin)


class ModelFieldGenerator(DecimalFieldMixin, CommonFieldGeneratorMixin):
    # Default django model field names.
    BOOLEAN = 'models.BooleanField'
    CHAR = 'models.CharField'
    DATETIME = 'models.DateTimeField'
    DATE = 'models.DateField'
    DECIMAL = 'models.DecimalField'
    EMAIL = 'models.EmailField'
    FOREIGN_KEY = 'models.ForeignKey'
    INTEGER = (
        "(models.BigIntegerField "
        "if getattr(settings, 'MDM_MODELS_BIGINT_ON', False) "
        "else models.IntegerField)")
    JSON = 'models.JSONField'
    UUID = 'models.UUIDField'

    # Additional options.
    DEFAULT_FIELD = JSON

    # Schema and django model strings` field name mapping.
    STRING_FORMAT_TO_FIELD_NAME = {
        'date': DATE,
        'date-time': DATETIME,
        'email': EMAIL,
        'uuid': UUID}

    DB_INDEX_FIELDS = ('created', 'updated', 'deleted', 'is_deleted')
    DB_INDEX_KWARGS = {'db_index': True}
    UUID_NOT_USED_PARAMS = ('null', 'blank', 'editable', 'default')
    DEFAULT_UUID_KWARGS = {'primary_key': True}

    _schema: Optional[dict] = None
    if _schema is None:
        _schema = {}

    _name = None
    _model_name = None
    _tag_groups = None
    _app = None

    def __call__(
            self, schema: dict, name: str, model_name: str,
            tag_groups: list[dict], app: str,
            required_fields: List[str]) -> str:

        self._schema = schema
        self._name = name
        self._model_name = model_name
        self._tag_groups = tag_groups
        self._app = app
        self._required_fields = required_fields

        return self.definition  # type: ignore

    @property
    def no_clean_kwargs(self) -> dict:
        return {
            **self.default_kwargs,
            **self.choices_kwargs,
            **self.guid_kwargs,
            **self.type_kwargs,
            **self._name_kwargs}

    @property
    def clean_kwargs(self) -> dict:
        return self.clean_extra_guid_kwargs(  # type: ignore
            self.no_clean_kwargs)

    @property
    def default_kwargs(self) -> dict:
        return {
            'verbose_name': self.title,
            'help_text': self.description,
            **self.optional_kwargs,
            'default': None,
            'editable': False,
            'db_column': (
                f"'{self._name}' if {self._is_camelcase_enabled} else None")}

    @property
    def choices_kwargs(self) -> dict:
        kwargs = {}
        if self.schema_enum:
            choices_name = ModelChoicesGenerator.get_choices_name(
                to_field_name(self._name))  # type: ignore
            kwargs['choices'] = choices_name
        return kwargs

    @property
    def type_kwargs(self) -> dict:
        action = self._field_type_kwargs_mapping.get(self.type)
        # No raise because not all field types have specific kwargs.
        kwargs = action() if action else {}
        return kwargs  # type: ignore

    @property
    def _name_kwargs(self) -> dict:
        return {**self.DB_INDEX_KWARGS} if self._is_db_index_field else {}

    @property
    def type(self) -> str:
        if self.has_object_enums:
            field_type = self.FOREIGN_KEY
        else:
            field_type = self.field_type_mapping.get(
                self.schema_type, self.DEFAULT_FIELD)
        return field_type

    @property
    def optional_kwargs(self) -> dict:
        return {
            'blank': self.is_blank_kwarg,
            'null': self.is_null_kwarg}

    @property
    def _is_camelcase_enabled(self) -> str:
        return "getattr(settings, 'MDM_MODELS_CAMEL_CASE', False)"

    @property
    def _is_db_index_field(self) -> bool:
        return self._name in self.DB_INDEX_FIELDS

    @property
    def _field_type_kwargs_mapping(self) -> dict:
        """ Not all field types have specific kwargs """

        return {
            self.INTEGER: self._get_integer_kwargs,
            self.DECIMAL: self._get_decimal_kwargs,
            self.CHAR: self._get_char_kwargs,
            self.FOREIGN_KEY: self._get_fk_kwargs,
            self.JSON: self._get_json_field_kwargs}

    def _get_integer_kwargs(self) -> dict:
        validators = self._get_value_range_validators()
        return {'validators': validators} if validators else {}

    def _get_value_range_validators(
            self, field_type: Optional[str] = None,
            coerce_to_string: Optional[bool] = False) -> Optional[str]:

        """
        Get MinValueValidator and MaxValueValidator string generated as
        Django field `validators` kwarg value
        >>> field_generator = ModelFieldGenerator()
        >>> field_generator._schema = {'minimum': -100}
        >>> field_generator._get_value_range_validators()
        '[MinValueValidator(-100)]'
        >>> field_generator._schema = {'maximum': 999}
        >>> field_generator._get_value_range_validators()
        '[MaxValueValidator(999)]'
        >>> field_generator._schema = {'minimum': -100, 'maximum': 999}
        >>> field_generator._get_value_range_validators()
        '[MinValueValidator(-100), MaxValueValidator(999)]'
        >>> field_generator._schema = {'minimum': -100.01}
        >>> field_generator._get_value_range_validators('Decimal', True)
        "[MinValueValidator(Decimal('-100.01'))]"
        >>> field_generator._schema = {'maximum': -999}
        >>> field_generator._get_value_range_validators('int', False)
        '[MaxValueValidator(int(-999))]'
        >>> field_generator._schema = {'other_field': -999}
        >>> field_generator._get_value_range_validators('int', False) is None
        True
        >>> field_generator._schema = {'minimum': 0}
        >>> field_generator._get_value_range_validators()
        '[MinValueValidator(0)]'
        >>> field_generator._schema = {'maximum': 0.0}
        >>> field_generator._get_value_range_validators()
        '[MaxValueValidator(0.0)]'
        """

        validators = []
        to_string = (
            lambda x: f'\'{x}\''  # noqa: unnecessary-lambda-assignment
            if coerce_to_string else x)
        to_arg = (
            lambda x: f'{field_type}(' # noqa: unnecessary-lambda-assignment
                      f'{x})'
            if field_type else f'{x}')
        if 'minimum' in self._schema:  # type: ignore
            validators.append(
                f'MinValueValidator('  # type: ignore
                f'{to_arg(to_string(self._schema["minimum"]))})')
        if 'maximum' in self._schema:  # type: ignore
            validators.append(
                f'MaxValueValidator('  # type: ignore
                f'{to_arg(to_string(self._schema["maximum"]))})')
        return f'[{", ".join(validators)}]' if validators else None

    def _get_decimal_kwargs(self) -> dict:
        kwargs = {}
        validators = self._get_value_range_validators(
            field_type='Decimal',
            coerce_to_string=True)
        if validators:
            kwargs['validators'] = validators
        decimal_places = self.decimal_places
        kwargs = {
            **kwargs,
            'max_digits': self.get_decimal_max_digits(decimal_places),
            'decimal_places': decimal_places}
        return kwargs

    def _get_char_kwargs(self) -> dict:
        return {
            'max_length': self._schema.get(  # type: ignore
                'maxLength', self.DEFAULT_CHAR_MAX_LENGTH)}

    def _get_fk_kwargs(self) -> dict:
        kwargs = {}
        if self._fk_related_model:
            kwargs['to'] = repr(self._fk_related_model)
        db_column = (
            f"'{self._name}GUID' if {self._is_camelcase_enabled} else None")
        kwargs = {
            **kwargs,
            'db_column': db_column,
            'on_delete': 'models.CASCADE',
            'related_name': repr(
                f'{self._model_name.lower()}_'  # type: ignore
                f'{self._name.lower()}')}
        return kwargs

    @property
    def _fk_related_model(self) -> str:
        to_app, to_model = self._get_model_app()
        return (
            self._get_fk_to_kwarg_value(to_app, to_model)  # type: ignore
            if to_app and to_model else None)

    def _get_model_app(self) -> Tuple[str, str]:
        """ Returns the tuple with format (app_label, model_name) """

        model_apps = [
            (group['name'], self.fk_model_name)
            for group in self._tag_groups  # type: ignore
            if self.fk_model_name in group['tags']]
        return model_apps[0] if model_apps else [None, None]  # type: ignore

    def _get_fk_to_kwarg_value(self, to_app: str, to_model: str) -> str:
        """
        >>> self = ModelFieldGenerator()
        >>> self._app = 'app1'; to_app = 'app1'; to_model = 'Model1'
        >>> self._get_fk_to_kwarg_value(to_app, to_model)
        'Model1'
        >>> self._app = 'app1'; to_app = 'app2'; to_model = 'Model1'
        >>> self._get_fk_to_kwarg_value(to_app, to_model)
        'app2.Model1'
        >>> self._app = 'app2'; to_app = 'app1'; to_model = 'Model1'
        >>> self._get_fk_to_kwarg_value(to_app, to_model)
        'app1.Model1'
        """

        to_app_lower = to_app.lower()
        is_current_app = to_app_lower != self._app.lower()  # type: ignore
        to_app = f'{to_app_lower}.' if is_current_app else ''

        return f'{to_app}{to_model}'

    def _get_json_field_kwargs(self) -> dict:
        kwargs = {}
        items = self._schema.get('items')  # type: ignore
        if items and isinstance(items, dict) and items.get('title'):
            kwargs['verbose_name'] = repr(items.get('title'))
        kwargs['default'] = 'dict'
        return kwargs


class ModelChoicesGenerator:
    def __call__(self, definition: dict) -> dict:
        choices = {}
        for prop_name, prop in definition['properties'].items():
            if prop.get('enum'):
                field_name = to_field_name(prop_name)
                if field_name == 'type':
                    continue
                choices_name = self.get_choices_name(field_name)
                choices[choices_name] = self.to_choices_args(prop)
        return choices

    @staticmethod
    def get_choices_name(field_name: str) -> str:
        return f'{field_name.upper()}_CHOICES'

    @staticmethod
    def to_choices_args(schema: dict) -> str:
        enums = (
            convert_strings_to_python_objects(
                schema.get('enum')))  # type: ignore
        labels = schema.get('x-enumNames', enums)
        return ", ".join(
            f"({repr(enum)}, _({repr(label)}))"
            for enum, label in zip(enums, labels))
