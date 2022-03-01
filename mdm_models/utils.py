import types
from typing import List, NoReturn

from pik.api.lazy_field import LazyField


MODELS = {}
BASE_SERIALIZERS = {}
SERIALIZERS = {}


def define_models(
    names: List[str],
    base_module: types.ModuleType,
    variables: dict,
) -> NoReturn:
    """Define Django models dynamically using its names and module with its base models provided"""

    for name in names:
        base_model = getattr(base_module, f'Base{name}')
        variables[name] = type(
            name, (base_model,), {'__module__': variables['__name__']})
        MODELS[f'{variables[name].__module__}.{name}'] = variables[name]
        serializer_name = f'{name}Serializer'
        BASE_SERIALIZERS[f'Base{serializer_name}'] = (
            f'{variables[name].__module__.replace(".models", ".serializers")}.{serializer_name}')


def _process_lazy_fields(new_serializer):
    """Process all serializer LazyFields and replace its path attributes from BaseSerializers to specific ones"""

    for field_name, field in new_serializer._declared_fields.items():
        if not isinstance(field, LazyField):
            continue
        old_path = getattr(field, 'path')
        if not old_path.startswith('Base'):
            # Already LazyField full path has been set.
            continue
        new_path = BASE_SERIALIZERS[old_path]
        field._kwargs['path'] = new_path
    return new_serializer


def define_serializers(
    names: List[str],
    base_module: types.ModuleType,
    variables: dict,
    model_module: types.ModuleType,
) -> NoReturn:
    """Define DRF serializers dynamically using its model names and module with its base serializers provided"""

    for name in names:
        new_serializer_name = f'{name}Serializer'
        base_serializer = getattr(base_module, f'Base{new_serializer_name}')
        model = getattr(model_module, name)
        attrs = {'__module__': variables['__name__']}
        # Set up `Meta` class
        meta = type('Meta', (base_serializer.Meta,), attrs)
        setattr(meta, 'model', model)
        new_serializer = type(
            new_serializer_name, (base_serializer,), attrs)
        setattr(new_serializer, 'Meta', meta)
        new_serializer = _process_lazy_fields(new_serializer)
        new_serializer_full_path = f'{new_serializer.__module__}.{new_serializer_name}'
        variables[new_serializer_name] = new_serializer
        SERIALIZERS[new_serializer_full_path] = new_serializer
