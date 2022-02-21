from typing import List, Optional


class SerializerFieldGenerator:
    # Default django serializer field names.
    UUID_SERIALIZER_FIELD_NAME = 'serializers.UUIDField'
    DATE_SERIALIZER_FIELD_NAME = 'serializers.DateField'
    DATETIME_SERIALIZER_FIELD_NAME = 'serializers.DateTimeField'
    FOREIGN_KEY_SERIALIZER_FIELD_NAME = 'serializers.PrimaryKeyRelatedField'
    INTEGER_SERIALIZER_FIELD_NAME = 'serializers.IntegerField'
    JSON_SERIALIZER_FIELD_NAME = 'serializers.JSONField'
    CHAR_SERIALIZER_FIELD_NAME = 'serializers.CharField'
    BOOLEAN_SERIALIZER_FIELD_NAME = 'serializers.BooleanField'
    DECIMAL_SERIALIZER_FIELD_NAME = 'serializers.DecimalField'
    CHOICES_SERIALIZER_FIELD_NAME = 'serializers.ChoiceField'

    # Additional options.
    DEFAULT_SERIALIZER_FIELD_NAME = JSON_SERIALIZER_FIELD_NAME
    DEFAULT_CHAR_SERIALIZER_FIELD_MAX_LENGTH = 255
    DEFAULT_DECIMAL_SERIALIZER_FIELD_DECIMAL_PLACES = 2
    DEFAULT_DECIMAL_SERIALIZER_FIELD_MAX_DIGITS = 10

    # Schema and django serializer field name mapping.
    STRING_TYPE = 'string'
    DECIMAL_TYPE = 'number'
    INTEGER_TYPE = 'integer'
    BOOLEAN_TYPE = 'boolean'

    # Schema and django serializer strings` field name mapping.
    STRING_FORMAT_TO_FIELD_NAME = {
        'uuid': UUID_SERIALIZER_FIELD_NAME,
        'date': DATE_SERIALIZER_FIELD_NAME,
        'date-time': DATETIME_SERIALIZER_FIELD_NAME,
    }

    # Nullable field options.
    DEFAULT_FIELD_KWARGS = {
        'allow_null': True,
    }

    @staticmethod
    def _to_python_kwargs(val: dict) -> str:
        """
        >>> SerializerFieldGenerator._to_python_kwargs({'foo': 1})
        'foo=1'
        >>> SerializerFieldGenerator._to_python_kwargs({'foo': 1, 'b': 'xx'})
        'foo=1, b=xx'
        >>> SerializerFieldGenerator._to_python_kwargs({})
        ''
        """
        return ', '.join([f"{k}={v}" for k, v in val.items()])

    @staticmethod
    def get_field_ref(schema: dict) -> Optional[str]:
        if '$ref' in schema:
            return schema['$ref']
        try:
            return next(
                item['$ref']
                for keyword in ['oneOf', 'anyOf', 'allOf'] if keyword in schema
                for item in schema[keyword] if '$ref' in item)
        except StopIteration:
            return None

    def _get_field_name_from_format(self, field_format: str) -> str:
        """ Get django serializer field name according to a schema string field format"""

        return self.STRING_FORMAT_TO_FIELD_NAME.get(
            field_format, self.CHAR_SERIALIZER_FIELD_NAME,
        )

    def _get_field_args(self, schema: dict, field_name: str) -> List[str]:
        """Get django ref serializer names"""

        if field_name == self.FOREIGN_KEY_SERIALIZER_FIELD_NAME:
            ref = self.get_field_ref(schema)
            serializer_ref = ref.split('/')[-1]
            try:
                domain = next(
                    schema.get(key)[0].get('x-domain')
                    for key in ('oneOf', 'anyOf', 'allOf')
                    if schema.get(key))
            except StopIteration:
                domain = None
            if domain:
                return [f"'{domain.lower()}.{serializer_ref}'"]
            return [f"'{serializer_ref}'"]
        return []

    def _get_field_kwargs(  # noqa: too-complex
            self, schema: dict, serializer_field_name: str, name: str, serializer_name: str, required: List[str],
    ) -> dict:
        """Get django serializer field kwargs options"""

        label = schema.get('title')
        if label:
            # IF field name in API start's with underscore.
            # It will have title starting with white space.
            # Probably a bug in schema generation.
            label = label.lstrip()
            label = label.lstrip('_')
        kwargs = {
            'label': repr(label),
            'allow_blank': name not in required,
        }
        choices = schema.get('enum')
        choice_names = schema.get('x-enumNames')
        if choices:
            kwargs['choices'] = repr(tuple(choices))
            if choice_names:
                kwargs['choices'] = repr(tuple(zip(choices, choice_names)))
            else:
                kwargs['choices'] = repr(tuple(zip(choices, choices)))
        help_text = schema.get('description')
        if help_text:
            # IF field name in API start's with underscore.
            # It will have title starting with white space.
            # Probably a bug in schema generation.
            help_text = help_text.lstrip()
            help_text = help_text.lstrip('_')
            kwargs['help_text'] = repr(help_text)
        kwargs.update(self.DEFAULT_FIELD_KWARGS)
        if name in ('_uid', 'guid', 'uid'):
            # kwargs['primary_key'] = True
            kwargs.pop('allow_null', None)
            kwargs['read_only'] = True
        if serializer_field_name == self.DECIMAL_SERIALIZER_FIELD_NAME:
            kwargs['max_digits'] = self.DEFAULT_DECIMAL_SERIALIZER_FIELD_MAX_DIGITS
            kwargs['decimal_places'] = (
                self.DEFAULT_DECIMAL_SERIALIZER_FIELD_DECIMAL_PLACES)
        if serializer_field_name == self.BOOLEAN_SERIALIZER_FIELD_NAME:
            kwargs.pop('allow_blank', None)
        if serializer_field_name == self.INTEGER_SERIALIZER_FIELD_NAME:
            kwargs.pop('allow_blank', None)
        if serializer_field_name == self.DECIMAL_SERIALIZER_FIELD_NAME:
            kwargs.pop('allow_blank', None)
        if serializer_field_name == self.CHAR_SERIALIZER_FIELD_NAME:
            kwargs['max_length'] = schema.get(
                'maxLength', self.DEFAULT_CHAR_SERIALIZER_FIELD_MAX_LENGTH)
        elif serializer_field_name in self.STRING_FORMAT_TO_FIELD_NAME.values():
            kwargs.pop('allow_null', None)
            kwargs.pop('allow_blank', None)
        elif serializer_field_name == self.FOREIGN_KEY_SERIALIZER_FIELD_NAME:
            # kwargs['on_delete'] = 'serializers.CASCADE'  # models.CASCADE
            # kwargs['related_name'] = repr(f'{serializer_name.lower()}_{name}')
            kwargs['many'] = True
        elif serializer_field_name == self.JSON_SERIALIZER_FIELD_NAME:
            items = schema.get('items')
            if items and isinstance(items, dict) and items.get('title'):
                kwargs['help_text'] = repr(items.get('title'))
            kwargs.pop('allow_null', None)
            kwargs.pop('allow_blank', None)
            kwargs['default'] = 'dict'
        return kwargs

    def _construct_field_definition(
            self, serializer_field_name, field_args, field_kwargs,
    ) -> str:

        args = ''
        if field_args:
            args = ", ".join(field_args) + ', '
        kwargs = self._to_python_kwargs(field_kwargs)
        return f"{serializer_field_name}({args}{kwargs})"

    def get_serializer_field_name(self, schema: dict) -> str:
        """Returns django field name by the schema key"""

        property_type = schema.get('type')
        refs = self.get_field_ref(schema)
        if refs:
            serializer_field_name = self.FOREIGN_KEY_SERIALIZER_FIELD_NAME
        elif schema.get('enum'):
            serializer_field_name = self.CHOICES_SERIALIZER_FIELD_NAME
        elif property_type == self.STRING_TYPE:
            field_format = schema.get('format', 'unknown')
            serializer_field_name = self._get_field_name_from_format(field_format)
        elif property_type == self.INTEGER_TYPE:
            serializer_field_name = self.INTEGER_SERIALIZER_FIELD_NAME
        elif property_type == self.BOOLEAN_TYPE:
            serializer_field_name = self.BOOLEAN_SERIALIZER_FIELD_NAME
        elif property_type == self.DECIMAL_TYPE:
            serializer_field_name = self.DECIMAL_SERIALIZER_FIELD_NAME
        else:
            serializer_field_name = self.DEFAULT_SERIALIZER_FIELD_NAME
        return serializer_field_name

    def __call__(self, schema: dict, name: str, serializer_name: str, required: List[str]):
        serializer_field_name = self.get_serializer_field_name(schema)
        args = self._get_field_args(schema, serializer_field_name)
        kwargs = self._get_field_kwargs(
            schema, serializer_field_name, name, serializer_name, required)
        return self._construct_field_definition(serializer_field_name, args, kwargs)
