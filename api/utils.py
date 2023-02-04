from django.apps import apps
from django.db.models import Model
from django.db.models.query import QuerySet
from django.db.models.base import ModelBase
from typing import Type, Union
from datetime import datetime

# https://docs.djangoproject.com/en/4.1/ref/models/fields/#field-types
# BASIC TYPE FIELDS
from django.db.models.fields import AutoField, BigAutoField, BigIntegerField, IntegerField, PositiveBigIntegerField, PositiveIntegerField, PositiveSmallIntegerField, SmallAutoField, SmallIntegerField # INT
from django.db.models.fields import BinaryField # BINARY
from django.db.models.fields import BooleanField # BOOLEAN
from django.db.models.fields import CharField, TextField, EmailField, SlugField, URLField, UUIDField # STR
from django.db.models.fields import DecimalField # DECIMAL
from django.db.models.fields import FloatField # FLOAT
from django.db.models        import JSONField # DICT
# COMPLEX TYPE FIELDS
from django.db.models.fields import DateTimeField # DATETIME
from django.db.models.fields import DateField # DATETIME:DATE
from django.db.models.fields import TimeField # DATETIME.TIME
from django.db.models.fields import DurationField # DATETIME.TIMEDELTA
# UNKNOWN TYPE FIELDS
from django.db.models        import FileField
from django.db.models.fields import FilePathField
from django.db.models.fields import GenericIPAddressField
from django.db.models        import ImageField
# RELATIONSHIP FIELDS
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.related import ManyToManyField, OneToOneField


hidden_models = [
    'logentry', 'permission', 'session', 'contenttype'
]

hidden_fields = [
    
]


fields_basic_types = (
    AutoField, BigAutoField, BigIntegerField, IntegerField, PositiveBigIntegerField, PositiveIntegerField, PositiveSmallIntegerField, SmallAutoField, SmallIntegerField, # INT
    BinaryField,  # BINARY
    BooleanField, # BOOLEAN
    CharField, TextField, EmailField, SlugField, URLField, UUIDField, # STR
    DecimalField, # DECIMAL
    FloatField, # FLOAT
    JSONField, # DICT
)

fields_complex_types = (
    DateTimeField, # DATETIME
    DateField, # DATETIME:DATE
    TimeField, # DATETIME.TIME
    DurationField, # DATETIME.TIMEDELTA
)

fields_unknown_types = (
    FileField, FilePathField, GenericIPAddressField, ImageField
)

fields_relationship_fields = (
    ForeignKey, ManyToManyField, OneToOneField
)

T_Basic = Union[int, float, bool, str]

class NotImplementedException(Exception):
    '''Not yet implemented'''
    pass

class UnknownFieldTypeException(Exception):
    '''Field type has not been accounted for'''
    pass


def get_models() -> dict[str, Type[Model]]:
    models = { model.__name__.lower():model for model in apps.get_models() }
    models = { k:v for k, v in models.items() if k not in hidden_models }
    return models


def find_models_by_name(model_name: str, all: bool=True, query_params: Union[None, dict[str, str]]=None) -> Union[QuerySet, Model, ModelBase, None]:
    models_abstract = get_models()

    if model_name not in models_abstract: return None

    model_abstract = models_abstract[model_name]

    if not query_params:
        models = models_abstract.objects
    else:
        fields = { f.name:f for f in model_abstract._meta.get_fields() if f.name in dir(model_abstract) and f.name not in hidden_fields }
        filter_kwargs = { k:v for k, v in query_params.items() if k in fields }
        models = models_abstract.objects.filter(**filter_kwargs)
    
    if all:
        return models.all()
    else:
        return models.first()


def model_to_json(model: Model, models_abstract: Union[None, dict[str, Type[Model]]]=None) -> Union[dict[str, Union[T_Basic, list[T_Basic]]], None]:
    if not models_abstract:
        models_abstract = get_models
    fields = [f.name for f in model._meta.get_fields() if f.name in dir(model) and f.name not in hidden_fields]
    
    res_obj = dict()
    for field in fields:
        attr = getattr(model, field)
        if isinstance(attr, fields_basic_types):
            res_obj[field] = attr
        elif isinstance(attr, fields_complex_types):
            if isinstance(attr, DateTimeField):
                res_obj[field] = attr.strftime('%Y-%m-%d %H-%M-%S')
            else:
                raise NotImplementedException
        elif isinstance(attr, fields_relationship_fields):
            if isinstance(attr, ForeignKey):
                raise NotImplementedException
            elif isinstance(attr, OneToOneField):
                res_obj[field] = model_to_json(attr, models_abstract=models_abstract)
            elif isinstance(attr, ManyToManyField):
                res_obj[field] = list()
                for s in attr.all():
                    res_obj[field].append(model_to_json(s, models_abstract=models_abstract))
            else:
                raise Exception('This is not supposed to be possible')
        elif isinstance(attr, fields_unknown_types):
            raise NotImplementedException
        else:
            raise UnknownFieldTypeException

    return res_obj

