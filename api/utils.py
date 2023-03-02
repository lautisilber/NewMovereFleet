import sys
import inspect
from rest_framework import serializers


def get_all_classes_from_module(module: str) -> list[any]:
    classes = [obj for name, obj in inspect.getmembers(sys.modules[module]) if inspect.isclass(obj)]
    return classes

def get_all_serializers_from_module(module: str) -> dict[str, serializers.ModelSerializer]:
    classes = {obj.url_name:obj for obj in get_all_classes_from_module(module) if issubclass(obj, serializers.ModelSerializer) and hasattr(obj, 'url_name')}
    return classes