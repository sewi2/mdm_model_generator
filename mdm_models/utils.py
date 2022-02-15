from typing import List, NoReturn


def define_models(models: List[str]) -> NoReturn:
    for model in models:
        try:
            from .models_based import model
        except ImportError:
            pass
        pass


def define_serializers(serializers: List[str]) -> NoReturn:
    pass
