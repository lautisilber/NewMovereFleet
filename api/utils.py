import functools
import inspect
from collections.abc import Mapping
from django.core.exceptions import ObjectDoesNotExist
from django.apps import apps
from django.db.models import Model
from django.db.models.query import QuerySet
from django.db.models.base import ModelBase
from typing import Type, Union, Any
import datetime
from django.forms import Field
from django.db.models.fields.related import ForeignObjectRel

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
    'logentry', 'password'
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
basic_types = (
    int, bytes, bool, str, float, dict, list
)

fields_complex_types = (
    DateTimeField, # DATETIME
    DateField, # DATETIME:DATE
    TimeField, # DATETIME.TIME
    DurationField, # DATETIME.TIMEDELTA
)
complex_types = (
    datetime.datetime, datetime.date, datetime.time, datetime.timedelta
)

fields_unknown_types = (
    FileField, FilePathField, GenericIPAddressField, ImageField
)

fields_relationship_fields = (
    ForeignKey, ManyToManyField, OneToOneField
)
relationship_types = (
    Model
)

T_Basic = Union[int, float, bool, str]

class NotImplementedException(Exception):
    '''Not yet implemented'''
    pass

class UnknownFieldTypeException(Exception):
    '''Field type has not been accounted for'''
    pass




### modified from https://github.com/lautisilber/NewMovereFleet/blob/main/api/utils.py ###
def is_simple_callable(obj):
    """
    True if the object is a callable that takes no arguments.
    """
    if not callable(obj):
        return False

    # Bail early since we cannot inspect built-in function signatures.
    if inspect.isbuiltin(obj):
        raise Exception(
            'Built-in function signatures are not inspectable. '
            'Wrap the function call in a simple, pure Python function.')

    if not (inspect.isfunction(obj) or inspect.ismethod(obj) or isinstance(obj, functools.partial)):
        return False

    sig = inspect.signature(obj)
    params = sig.parameters.values()
    return all(
        param.kind == param.VAR_POSITIONAL or
        param.kind == param.VAR_KEYWORD or
        param.default != param.empty
        for param in params
    )


def get_attribute(instance: Any, attr: str):
    """
    Similar to Python's built in `getattr(instance, attr)`,
    but takes a list of nested attributes, instead of a single attribute.
    Also accepts either attribute lookup on objects or dictionary lookups.
    """
    try:
        if isinstance(instance, Mapping):
            instance = instance[attr]
        else:
            instance = getattr(instance, attr)
    except ObjectDoesNotExist:
        return None
    if is_simple_callable(instance):
        try:
            instance = instance()
        except (AttributeError, KeyError) as exc:
            # If we raised an Attribute or KeyError here it'd get treated
            # as an omitted field in `Field.get_attribute()`. Instead we
            # raise a ValueError to ensure the exception is not masked.
            raise ValueError('Exception raised in callable attribute "{}"; original exception was: {}'.format(attr, exc))

    return instance
###


def get_models() -> dict[str, Type[Model]]:
    models = { model.__name__.lower():model for model in apps.get_models() }
    models = { k:v for k, v in models.items() if k not in hidden_models }
    return models


def get_fields(model: Union[Type[Model], Type[ModelBase]]) -> dict[str, Field, ForeignObjectRel]:
    return { f.name:f for f in model._meta.get_fields() if f.name not in hidden_fields }


def find_models_by_name(model_name: str, all: bool=True, query_params: Union[None, dict[str, str]]=None) -> Union[QuerySet, Type[Model], Type[ModelBase], None]:
    models_abstract = get_models()

    if model_name not in models_abstract: return None

    model_abstract = models_abstract[model_name]

    if not query_params:
        models = model_abstract.objects
    else:
        fields = { f.name:f for f in model_abstract._meta.get_fields() if f.name in dir(model_abstract) and f.name not in hidden_fields }
        filter_kwargs = { k:v for k, v in query_params.items() if k in fields }
        models = model_abstract.objects.filter(**filter_kwargs)
    
    if all:
        return models.all()
    else:
        return models.first()


ModelJSON = dict[str, Union[T_Basic, list[T_Basic]]]

def _model_to_json(model: Type[Model], models_abstract: Union[None, dict[str, Type[Model]]]=None) -> Union[ModelJSON, None]:
    if not models_abstract:
        models_abstract = get_models()
    fields = get_fields(model)
    
    res_obj = dict()
    for nfield, field in fields.items():
        attr = get_attribute(model, nfield)
        # if isinstance(field, fields_basic_types):
        #     res_obj[field] = attr
        # elif isinstance(field, fields_complex_types):
        #     if isinstance(field, DateTimeField):
        #         res_obj[field] = attr.strftime('%Y-%m-%d %H-%M-%S')
        #     else:
        #         raise NotImplementedException
        # elif isinstance(field, fields_relationship_fields):
        #     if isinstance(field, OneToOneField):
        #         res_obj[field] = _model_to_json(attr, models_abstract=models_abstract)
        #     elif isinstance(field, ManyToManyField):
        #         res_obj[field] = list()
        #         for s in attr.all():
        #             res_obj[field].append(_model_to_json(s, models_abstract=models_abstract))
        #     elif isinstance(field, ForeignKey):
        #         raise NotImplementedException(f'obj: {attr}, type: {type(attr)}\nfield: {field}, type {type(field)}')
        #     else:
        #         raise Exception(f'This is not supposed to be possible\nobj: {attr}, type: {type(attr)}\nfield: {field}, type {type(field)}')
        # elif isinstance(field, fields_unknown_types):
        #     raise NotImplementedException(f'obj: {attr}, type: {type(attr)}\nfield: {field}, type {type(field)}')
        # else:
        #     raise UnknownFieldTypeException(f'obj: {attr}, type: {type(attr)}\nfield: {field}, type {type(field)}')
        if isinstance(attr, basic_types):
            res_obj[nfield] = attr
        elif isinstance(attr, complex_types):
            if isinstance(attr, datetime.datetime):
                res_obj[nfield] = attr.strftime('%Y-%m-%d %H-%M-%S')
            else:
                raise NotImplementedException(f'types date, time and timedelta have not yet been implemented\nfname: {nfield}, type: {type(attr)}')
        elif isinstance(attr, Model):
                res_obj[nfield+'-id'] = attr.id
        else:
            if hasattr(attr, 'all'):
                if is_simple_callable(attr.all):
                    _attr = attr.all()
                    if isinstance(_attr, QuerySet): # it is a many-to-many or one-to-many relationship
                        res_obj[nfield+'-id'] = list()
                        for model in _attr:
                            if isinstance(model, Model):
                                res_obj[nfield+'-id'].append(model.id)
                            else:
                                raise Exception
                    else:
                        UnknownFieldTypeException
                else:
                    UnknownFieldTypeException
            else:
                UnknownFieldTypeException

    return res_obj


def model_to_json(model: str, all: bool, query_params: Union[dict[str, str], None]=None) -> Union[list[Union[ModelJSON, None]], ModelJSON, None]:
    models = find_models_by_name(model, all, query_params)
    if models is None:
        return None
    if all:
        ret_obj = list()
        for model in models:
            ret_obj.append(_model_to_json(model))
        return ret_obj
    return _model_to_json(models)


def json_to_model(model_abstract: str, params: dict) -> dict:
    models_abstract = get_models()
    if not model_abstract in models_abstract:
        return {'error': 'Model name was not found'}
    
    model_abstract: Type[Model] = models_abstract[model_abstract]
    fields = get_fields(model_abstract)
    params = { k:v for k, v in params.items() if k in fields.keys() }
    fields_to_remove: list(str) = list()
    for k in params:
        if isinstance(fields[k], DateTimeField):
            params[k] = datetime.strptime(params[k], '%Y-%m-%d_%H-%M-%S')
        elif isinstance(fields[k], ForeignKey):
            try:
                params[k] = fields[k].related_model.objects.filter(id=params[k]).first()
            except:
                fields_to_remove.append(k)
    params = { k:v for k, v in params.items() if k not in fields_to_remove }

    try:
        model = model_abstract(**params)
        model.save()
    except Exception as err:
        return {'error': "Couldn't create model with given params", 'Traceback': str(err)}
    return {'OK': 'model was created'}

