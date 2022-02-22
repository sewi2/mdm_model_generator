import re
import types
from typing import List, NoReturn


MODELS = {}


def define_models(
    names: List[str],
    base_module: types.ModuleType,
    variables: dict,
) -> NoReturn:
    """Define Django models dynamically using its names and module with its base models provided"""

    for name, base in vars(base_module).items():
        match = re.match('Base(?P<name>.+)', name)
        if not match or match['name'] in variables or match['name'] not in names:
            continue

        variables[match['name']] = type(
            match['name'], (base,), {'__module__': variables['__name__']})
        MODELS[name] = variables[match['name']]


def define_serializers(
    names: List[str],
    base_module: types.ModuleType,
    variables: dict,
    model_module: types.ModuleType,
) -> NoReturn:
    """Define DRF serializers dynamically using its model names and module with its base serializers provided"""

    for name, base in vars(base_module).items():
        match = re.match('Base(?P<name>.+)', name)
        match_model_name = match['name'].split('Serializer')[0]
        match_serializer_name = match['name']
        if not match or match['name'] in variables or match_model_name not in names:
            continue

        model = getattr(model_module, match_model_name, None)
        if not model:
            raise LookupError(f"Cannot declare serializer. Model {match_model_name} doesn't exist")
        setattr(base.Meta, 'model', model)
        base.Meta.model = model
        variables[match_serializer_name] = type(
            match_serializer_name, (base,), {'__module__': variables['__name__']})
