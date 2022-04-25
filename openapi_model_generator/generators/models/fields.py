from typing import List, Optional, Iterable, Any


class ModelFieldGenerator:
    # Default django model field names.
    UUID_MODEL_FIELD_NAME = 'models.UUIDField'
    DATE_MODEL_FIELD_NAME = 'models.DateField'
    DATETIME_MODEL_FIELD_NAME = 'models.DateTimeField'
    FOREIGN_KEY_MODEL_FIELD_NAME = 'models.ForeignKey'
    INTEGER_MODEL_FIELD_NAME = 'models.IntegerField'
    JSON_MODEL_FIELD_NAME = 'models.JSONField'
    CHAR_MODEL_FIELD_NAME = 'models.CharField'
    BOOLEAN_MODEL_FIELD_NAME = 'models.BooleanField'
    DECIMAL_MODEL_FIELD_NAME = 'models.DecimalField'

    # Additional options.
    DEFAULT_MODEL_FIELD_NAME = JSON_MODEL_FIELD_NAME
    DEFAULT_CHAR_MODEL_FIELD_MAX_LENGTH = 255
    DEFAULT_DECIMAL_MODEL_FIELD_DECIMAL_PLACES = 2
    DEFAULT_DECIMAL_MODEL_FIELD_MAX_DIGITS = 10

    # Schema and django model field name mapping.
    STRING_TYPE = 'string'
    DECIMAL_TYPE = 'number'
    INTEGER_TYPE = 'integer'
    BOOLEAN_TYPE = 'boolean'

    # Schema and django model strings` field name mapping.
    STRING_FORMAT_TO_FIELD_NAME = {
        'uuid': UUID_MODEL_FIELD_NAME,
        'date': DATE_MODEL_FIELD_NAME,
        'date-time': DATETIME_MODEL_FIELD_NAME,
    }

    EXCLUDED_FIELD_NAMES = ['type', ]

    @staticmethod
    def _to_python_kwargs(val: dict) -> str:
        """
        >>> ModelFieldGenerator._to_python_kwargs({'foo': 1})
        'foo=1'
        >>> ModelFieldGenerator._to_python_kwargs({'foo': 1, 'b': 'xx'})
        'foo=1, b=xx'
        >>> ModelFieldGenerator._to_python_kwargs({})
        ''
        """
        return ', '.join([f"{k}={v}" for k, v in val.items()])

    def _get_field_name_from_format(self, field_format: str) -> str:
        """Get django model field name
        according to a schema string field format"""

        return self.STRING_FORMAT_TO_FIELD_NAME.get(
            field_format, self.CHAR_MODEL_FIELD_NAME,
        )

    @staticmethod
    def get_field_ref(schema: dict) -> Optional[str]:
        if '$ref' in schema:
            return schema['$ref']
        try:
            return next(
                item['$ref']
                for keyword in ['oneOf', 'anyOf', 'allOf']
                if keyword in schema
                for item in schema[keyword] if '$ref' in item)
        except StopIteration:
            return None

    def _get_field_args(self, schema: dict, field_name: str) -> List[str]:
        """Get django ref model names"""

        if field_name == self.FOREIGN_KEY_MODEL_FIELD_NAME \
                and self.get_field_ref(schema):
            ref = self.get_field_ref(schema)
            model_ref = ref.split('/')[-1]
            try:
                domain = next(
                    schema.get(key)[0].get('x-domain')
                    for key in ('oneOf', 'anyOf', 'allOf')
                    if schema.get(key))
            except StopIteration:
                domain = None
            if domain:
                return [f"'{domain.lower()}.{model_ref}'"]
            return [f"'{model_ref}'"]
        return []

    def _str_to_python(self, item: Any):
        mapping = {
            'true': True,
            'false': False,
            'none': None,
        }
        if isinstance(item, str) and item.lower() in mapping:
            return mapping.get(item.lower())
        return item

    def _to_python_value(self, iterable: Iterable):
        return list(map(self._str_to_python, iterable))

    def _get_field_kwargs(  # noqa: too-complex
            self, schema: dict, model_field_name: str,
            name: str, model_name: str, required: List[str],
    ) -> dict:
        """Get django model field kwargs options"""

        kwargs = {
            'verbose_name': repr(schema.get('title', '')),
            'help_text': repr(schema.get('description', '')),
            # TODO: Need to analyze and review.
            # 'blank': name not in required,
            # 'null': schema.get('nullable', False),
            'blank': True,
            'null': True,
            'editable': False,
        }
        if schema.get('enum'):
            enums = self._to_python_value(schema.get('enum'))
            kwargs['choices'] = (repr(tuple(zip(enums, enums)))
                                 if not schema.get('x-enumNames')
                                 else repr(tuple(zip(enums, schema
                                                     .get('x-enumNames')))))
        if name == 'guid':
            kwargs['primary_key'] = True
            kwargs.pop('null', None)
            kwargs.pop('blank', None)
            kwargs.pop('editable', None)
        if model_field_name == self.DECIMAL_MODEL_FIELD_NAME:
            kwargs['max_digits'] = self.DEFAULT_DECIMAL_MODEL_FIELD_MAX_DIGITS
            kwargs['decimal_places'] = (
                self.DEFAULT_DECIMAL_MODEL_FIELD_DECIMAL_PLACES)
        if model_field_name == self.CHAR_MODEL_FIELD_NAME:
            kwargs['max_length'] = schema.get(
                'maxLength', self.DEFAULT_CHAR_MODEL_FIELD_MAX_LENGTH)
        elif model_field_name == self.FOREIGN_KEY_MODEL_FIELD_NAME:
            enum = schema.get(
                'properties', {}).get('type', {}).get('enum', [])
            if enum and isinstance(enum, list):
                kwargs['to'] = repr(enum[0])
            kwargs['on_delete'] = 'models.CASCADE'
            kwargs['related_name'] = repr(
                f'{model_name.lower()}_{name.lower()}')
        elif model_field_name == self.JSON_MODEL_FIELD_NAME:
            items = schema.get('items')
            if items and isinstance(items, dict) and items.get('title'):
                kwargs['verbose_name'] = repr(items.get('title'))
            kwargs.pop('null', None)
            kwargs.pop('blank', None)
            kwargs['default'] = 'dict'
        if name in ('created', 'updated', 'deleted', 'is_deleted'):
            kwargs['db_index'] = True
        return kwargs

    def _construct_field_definition(
            self, model_field_name, field_args, field_kwargs,
    ) -> str:

        args = ''
        if field_args:
            args = ", ".join(field_args) + ', '
        kwargs = self._to_python_kwargs(field_kwargs)
        return f"{model_field_name}({args}{kwargs})"

    def get_model_field_name(self, schema: dict) -> str:
        """Returns django field name by the schema key"""

        property_type = schema.get('type')
        refs = self.get_field_ref(schema)
        if refs or (property_type == "object"
                    and schema.get('properties', {}).get(
                    'type', {}).get('enum', [])):
            model_field_name = self.FOREIGN_KEY_MODEL_FIELD_NAME
        elif property_type == self.STRING_TYPE:
            field_format = schema.get('format', 'unknown')
            model_field_name = self._get_field_name_from_format(field_format)
        elif property_type == self.INTEGER_TYPE:
            model_field_name = self.INTEGER_MODEL_FIELD_NAME
        elif property_type == self.BOOLEAN_TYPE:
            model_field_name = self.BOOLEAN_MODEL_FIELD_NAME
        elif property_type == self.DECIMAL_TYPE:
            model_field_name = self.DECIMAL_MODEL_FIELD_NAME
        else:
            model_field_name = self.DEFAULT_MODEL_FIELD_NAME
        return model_field_name

    def __call__(self, schema: dict, name: str,
                 model_name: str, required: List[str]):
        model_field_name = self.get_model_field_name(schema)
        args = self._get_field_args(schema, model_field_name)
        kwargs = self._get_field_kwargs(
            schema, model_field_name, name, model_name, required)
        return self._construct_field_definition(
            model_field_name, args, kwargs)
