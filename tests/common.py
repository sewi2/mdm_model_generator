import shutil
from pathlib import Path
from typing import Callable
from typing import Union, NoReturn

import simplejson as json

from mdm_model_generator.generators.models.fields import ModelFieldGenerator
from mdm_model_generator.generators.serializers.fields import (
    SerializerFieldGenerator)

SCHEMA_FILENAME = 'schema.json'
EXPECTED_RESULTS_MODELS_FILENAME = 'expected_model_properties.json'
EXPECTED_RESULTS_SERIALIZERS_FILENAME = 'expected_serializer_properties.json'


def load_json_file(file_path: Union[str, Path]) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        result = json.load(file, encoding='utf-8')
    return result


def rm_dir(dir_path: Union[str, Path]) -> NoReturn:
    try:
        shutil.rmtree(dir_path)
    except OSError as exception:
        print("Error: %s - %s." % (exception.filename, exception.strerror))


def print_diff_items(dcmp):
    for name in dcmp.diff_files:
        assert False, "diff_file `%s` found in `%s` and `%s`" % (
            name, dcmp.left, dcmp.right)
    for sub_dcmp in dcmp.subdirs.values():
        diff_left = (
            sorted(list(set(sub_dcmp.left_list) - set(sub_dcmp.right_list))))
        diff_right = (
            sorted(list(set(sub_dcmp.right_list) - set(sub_dcmp.left_list))))
        if sub_dcmp.left_list != sub_dcmp.right_list:
            assert False, (
                "\nDiff between catalog structure `%s` and `%s` \n"
                "found in `%s` and `%s` respectively. \n"
                "The diffs are `%s` and `%s` respectively.\n") % (
                sub_dcmp.left, sub_dcmp.right,
                sub_dcmp.left_list, sub_dcmp.right_list,
                diff_left, diff_right)
        print_diff_items(sub_dcmp)


class ModelGeneratorMixin:
    schema: dict = {}
    field_name: str = 'test_field'
    model_name: str = 'TestModel'
    tag_groups: list = []
    app: str = 'test'
    required_fields: list = []

    _generator: Callable = ModelFieldGenerator()
    _result_definition: str = _generator(
        schema=schema, name=field_name, model_name=model_name,
        tag_groups=tag_groups, app=app, required_fields=required_fields)

    _expected_results: dict = {}

    def test_properties(self):
        for prop_name, expected_value in self._expected_results.items():
            prop_value = getattr(self._generator, prop_name)
            assert prop_value == expected_value, prop_name


class SerializerGeneratorMixin:
    schema: dict = {}
    field_name: str = 'test_field'
    serializer_name: str = 'TestModelSerializer'
    tag_groups: list = []
    app: str = 'test'
    required_fields: list = []

    _generator: Callable = SerializerFieldGenerator()

    _expected_results: dict = {}
    _result_definition: str = _generator(
        schema=schema, name=field_name, serializer_name=serializer_name,
        required_fields=required_fields)

    def test_properties(self):
        for prop_name, expected_value in self._expected_results.items():
            prop_value = getattr(self._generator, prop_name)
            assert prop_value == expected_value, prop_name
