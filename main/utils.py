import sys
import inspect
from django.db import models


def get_all_classes_from_module(module: str) -> list[any]:
    classes = [obj for name, obj in inspect.getmembers(sys.modules[module]) if inspect.isclass(obj)]
    return classes

def get_all_models_from_module(module: str) -> list[type[models.Model]]:
    model_classes = [obj for obj in get_all_classes_from_module(module) if issubclass(obj, models.Model)]
    return model_classes

def get_all_nonabstract_models_from_module(module: str) -> dict[str, type[models.Model]]:
    models_urls = {models_class.url_name:models_class for models_class in get_all_models_from_module(module) if hasattr(models_class, 'url_name')}
    return models_urls
