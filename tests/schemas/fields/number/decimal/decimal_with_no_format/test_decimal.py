from pathlib import Path
from typing import Callable

from mdm_model_generator.generators.models.fields import ModelFieldGenerator
from mdm_model_generator.generators.serializers.fields import (
    SerializerFieldGenerator)
from tests.common import (
    SCHEMA_FILENAME, EXPECTED_RESULTS_MODELS_FILENAME,
    EXPECTED_RESULTS_SERIALIZERS_FILENAME, load_json_file,
    ModelGeneratorMixin, SerializerGeneratorMixin)


BASE_DIR = Path(__file__).parent
SCHEMA_FILEPATH = BASE_DIR / SCHEMA_FILENAME
SCHEMA = load_json_file(SCHEMA_FILEPATH)
EXPECTED_MODEL_PROPERTIES = load_json_file(
    BASE_DIR / EXPECTED_RESULTS_MODELS_FILENAME)
EXPECTED_SERIALIZER_PROPERTIES = load_json_file(
    BASE_DIR / EXPECTED_RESULTS_SERIALIZERS_FILENAME)


class TestModelGeneratorDecimalNotFormattedField(ModelGeneratorMixin):
    schema: dict = SCHEMA
    _generator: Callable = ModelFieldGenerator()
    _result_definition: str = _generator(
        schema=schema,
        name=ModelGeneratorMixin.field_name,
        model_name=ModelGeneratorMixin.model_name,
        tag_groups=ModelGeneratorMixin.tag_groups,
        app=ModelGeneratorMixin.app,
        required_fields=ModelGeneratorMixin.required_fields)
    _expected_results: dict = EXPECTED_MODEL_PROPERTIES

    def test_result_definition(self):
        assert self._result_definition == (
            'models.DecimalField(verbose_name=_(\'Число\'), '
            'help_text=_("Пример значения \'number\'"), blank=True, '
            'null=True, default=None, editable=False, '
            "db_column='test_field' if getattr(settings, "
            "'MDM_MODELS_CAMEL_CASE', False) "
            "else None, validators=[MinValueValidator("
            "Decimal('-1000000000000')), "
            "MaxValueValidator(Decimal('1000000000000'))], max_digits=17, "
            'decimal_places=4)')


class TestSerializerGeneratorDecimalNotFormattedField(
        SerializerGeneratorMixin):

    schema: dict = SCHEMA
    _expected_results: dict = EXPECTED_SERIALIZER_PROPERTIES
    _generator: Callable = SerializerFieldGenerator()
    _result_definition: str = _generator(
        schema=schema,
        name=SerializerGeneratorMixin.field_name,
        serializer_name=SerializerGeneratorMixin.serializer_name,
        required_fields=SerializerGeneratorMixin.required_fields)

    def test_result_definition(self):
        assert self._result_definition == (
            'serializers.DecimalField(label=_(\'Число\'), '
            'help_text=_("Пример значения '
            '\'number\'"), allow_null=True, max_digits=17, decimal_places=4, '
            'min_value=-1000000000000, max_value=1000000000000)')
