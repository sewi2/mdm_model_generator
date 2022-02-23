import types
from typing import List, NoReturn

from pik.api.lazy_field import LazyField


MODELS = {}
SERIALIZERS = {}


def define_models(
    names: List[str],
    base_module: types.ModuleType,
    variables: dict,
) -> NoReturn:
    """Define Django models dynamically using its names and module with its base models provided"""

    for name in names:
        base_model = getattr(base_module, f'Base{name}', None)
        if not base_model:
            raise LookupError(f"Cannot declare model. Base{name} doesn't exist")

        variables[name] = type(
            name, (base_model,), {'__module__': variables['__name__']})
        MODELS.update({f'{variables[name].__module__}.{name}': variables[name]})
        SERIALIZERS.update({f'{variables[name].__module__.replace(".models", ".serializers")}.{name}Serializer': None})


def _process_lazy_fields(new_serializer):
    """Process all serializer LazyFields and replace its path attributes from BaseSerializers to specific ones"""

    for field_name, field in new_serializer._declared_fields.copy().items():
        if not isinstance(field, LazyField):
            continue
        old_path = getattr(field, 'path', None)
        if not old_path:
            raise LookupError(f"Cannot find `path` attribute for LazyField "
                              f"{new_serializer.__module__}.{new_serializer.__name__}."
                              f"{field_name} , that must be declared.")
        if 'Base' != old_path[:len('Base')]:
            # Already LazyField full path has been set.
            continue
        ref_serializer_name = old_path[len('Base'):]
        ref_serializer_full_name = [key for key in SERIALIZERS.keys() if ref_serializer_name == key.split('.')[-1]]
        if not ref_serializer_full_name:
            raise LookupError(f"Cannot set LazyField path to serializer field "
                              f"{new_serializer.__module__}.{new_serializer.__name__}.{field_name}. "
                              f"{ref_serializer_name} doesn't exist")
        field._kwargs['path'] = ref_serializer_full_name[0]
    return new_serializer


def define_serializers(
    names: List[str],
    base_module: types.ModuleType,
    variables: dict,
    model_module: types.ModuleType,
) -> NoReturn:
    """Define DRF serializers dynamically using its model names and module with its base serializers provided"""

    for name in names:
        base_serializer = getattr(base_module, f'Base{name}Serializer', None)
        if not base_serializer:
            raise LookupError(f"Cannot declare serializer. Base{name}Serializer doesn't exist")
        model = getattr(model_module, name, None)
        if not model:
            raise LookupError(f"Cannot declare serializer. Model {name} doesn't exist")

        setattr(base_serializer.Meta, 'model', model)
        base_serializer.Meta.model = model
        new_serializer = type(
            f'{name}Serializer', (base_serializer,), {'__module__': variables['__name__']})

        new_serializer = _process_lazy_fields(new_serializer)
        variables[f'{name}Serializer'] = new_serializer
        SERIALIZERS.update({f"{new_serializer.__module__}.{name}Serializer": new_serializer})
