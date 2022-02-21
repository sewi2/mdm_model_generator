import inspect
import re
import types
from typing import List, Type, Optional, NoReturn

import django.db.models
from django.apps import apps
from rest_framework.serializers import BaseSerializer, Serializer


def _register_model(app_label: str, model: django.db.models.Model):
    """ Register Django app model silently"""

    try:
        apps.register_model(app_label, model)
    except RuntimeError:
        pass


def _get_app_model(
    app_label: str,
    model_name: str,
    require_ready=False,
) -> Optional[django.db.models.Model]:
    """ Get Django app model silently"""

    model = None
    try:
        model = apps.get_model(app_label, model_name, require_ready)
    except LookupError:
        pass
    return model


def define_models(
    names: List[str],
    base_module: types.ModuleType,
    variables: dict,
    base_class=django.db.models.Model,
) -> NoReturn:
    """Define Django models dynamically using its names and module with its base models provided"""

    def is_class_needed(item):
        return (
                inspect.isclass(item)
                and item.__module__ == base_module.__name__
                and issubclass(item, base_class))

    for name, base in inspect.getmembers(base_module, is_class_needed):
        match = re.match('Base(?P<name>.+)', name)
        if not match or match['name'] in variables or match['name'] not in names:
            continue

        variables[match['name']] = type(
            match['name'], (base,), {'__module__': variables['__name__']})
        _register_model(variables['__name__'].split('.models')[0], variables[match['name']])


def define_serializers(
    names: List[str],
    base_module: types.ModuleType,
    variables: dict,
    model_module: types.ModuleType,
    base_class: Type[BaseSerializer] = Serializer,
) -> NoReturn:
    """Define DRF serializers dynamically using its model names and module with its base serializers provided"""

    def is_class_needed(item):
        return (
                inspect.isclass(item)
                and item.__module__ == base_module.__name__
                and issubclass(item, base_class))

    _model_app_name = model_module.__name__.split('.models')
    model_app_name = _model_app_name[0]

    for name, base in inspect.getmembers(base_module, is_class_needed):
        match = re.match('Base(?P<name>.+)', name)
        match_model_name = match['name'].split('Serializer')[0]
        match_serializer_name = match['name']
        if not match or match['name'] in variables or match_model_name not in names:
            continue

        model = _get_app_model(model_app_name, match_model_name)
        if not model:
            raise LookupError(f"Cannot declare serializer. Model {match_model_name} doesn't exist")
        setattr(base.Meta, 'model', model)
        base.Meta.model = model
        variables[match_serializer_name] = type(
            match_serializer_name, (base,), {'__module__': variables['__name__']})


def define_missing_classes(base_module, variables, base_class):
    def is_model(item):
        return (
                inspect.isclass(item)
                and item.__module__ == base_module.__name__
                and issubclass(item, base_class))

    for name, base in inspect.getmembers(base_module, is_model):
        match = re.match('Base(?P<name>.+)', name)
        if not match or match['name'] in variables:
            continue

        variables[match['name']] = type(
            match['name'], (base,), {'__module__': variables['__name__']})
