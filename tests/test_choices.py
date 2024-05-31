from mdm_model_generator.generators.models.fields import (
    ModelChoicesGenerator, ModelFieldGenerator)
from mdm_model_generator.generators.serializers.fields import (
    SerializerFieldGenerator)


class TestChoices:
    app: str = 'test'
    model_name: str = 'TestModel'
    field_name: str = 'test_field'
    tag_groups: list = []
    required = []
    schema: dict = {
        'type': 'string',
        'title': 'Тестовое поле',
        'description': 'Поле для тестирования',
        'enum': ['val1', 'val2', 'val3'],
        'x-enumNames': ['Значение1', 'Значение2', 'Значение3'],
        'maxLength': 20,
        'nullable': True}
    definition = {'properties': {field_name: schema}}

    def test_choices_definition(self):
        choices = ModelChoicesGenerator()(self.definition)
        assert choices == {
            'TEST_FIELD_CHOICES':
                "('val1', _('Значение1')), "
                "('val2', _('Значение2')), "
                "('val3', _('Значение3'))"}

    def test_model_choices(self):
        model_field_definition = ModelFieldGenerator()(
            self.schema, self.field_name, self.model_name,
            self.tag_groups, self.app, self.required)
        assert model_field_definition == (
            "models.CharField(verbose_name=_('Тестовое поле'), "
            "help_text=_('Поле для тестирования'), blank=True, null=True, "
            "default=None, editable=False, db_column='test_field' "
            "if getattr(settings, 'MDM_MODELS_CAMEL_CASE', False) else None, "
            "choices=TEST_FIELD_CHOICES, max_length=20)")

    def test_serializer_choices(self):
        serializer_field_definition = SerializerFieldGenerator()(
            self.schema, self.field_name, self.model_name, self.required)
        assert serializer_field_definition == (
            "serializers.ChoiceField(label=_('Тестовое поле'), "
            "help_text=_('Поле для тестирования'), allow_blank=True, "
            "allow_null=True, "
            "choices=base_models.BaseTestModel.TEST_FIELD_CHOICES)")
