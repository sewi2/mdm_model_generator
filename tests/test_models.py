from pathlib import Path
from typing import Callable

from mdm_model_generator.generators.models.fields import ModelFieldGenerator
from tests.common import SCHEMA_FILENAME, load_json_file, ModelGeneratorMixin


BASE_DIR = Path(__file__).parent
SCHEMA_FILEPATH = BASE_DIR / SCHEMA_FILENAME
SCHEMA = load_json_file(SCHEMA_FILEPATH)
EXPECTED_MODEL_PROPERTIES = {}


class TestModelGeneratorBooleanField(ModelGeneratorMixin):
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

    def test_properties(self):
        self._expected_results['_field_type_kwargs_mapping'] = {
            'models.CharField': self._generator._get_char_kwargs,
            'models.DecimalField': self._generator._get_decimal_kwargs,
            'models.ForeignKey': self._generator._get_fk_kwargs,
            'models.IntegerField': self._generator._get_integer_kwargs,
            'models.JSONField': self._generator._get_json_field_kwargs}
