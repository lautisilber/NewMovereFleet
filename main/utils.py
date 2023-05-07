from datetime import datetime, timezone
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


### view renderers

from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponseNotFound, HttpResponseForbidden, HttpResponse
from django import forms
from django.contrib import messages
from typing import Any, Union


def model_view_create(request: HttpRequest, form_cls: type[forms.ModelForm], default_redirect: str='main-home') -> Union[forms.ModelForm, HttpResponse]:
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    if request.method == 'POST':
        form = form_cls(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Created {form.Meta.model.__name__}!')
            return redirect(request.GET.get('next', default_redirect))
    else:
        form = form_cls()
    return form

def model_view_update(request: HttpRequest, form_cls: type[forms.ModelForm], model_id: int, default_redirect: str='main-home') -> Union[forms.ModelForm, HttpResponse]:
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    model_cls = form_cls.Meta.model
    if not model_cls.objects.filter(id=model_id).exists():
        return HttpResponseNotFound(f'The {form.Meta.model.__name__} with id {model_id} was not found')
    model = model_cls.objects.get(id=model_id)
    if request.method == 'POST':
        form = form_cls(request.POST, instance=model)
        if form.is_valid():
            form.save()
            messages.info(request, f'Updated {form.instance.__class__.__name__}!')
            return redirect(request.GET.get('next', default_redirect))
    else:
        form = form_cls(instance=model)
    return form

def model_view_delete(request: HttpRequest, model_cls: type[models.Model], model_id: int, default_redirect: str='main-home') -> HttpResponse:
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    if not model_cls.objects.filter(id=model_id).exists():
        return HttpResponseNotFound(f'The {model_cls.__name__} with id {model_id} was not found')
    model = model_cls.objects.get(id=model_id)
    model.delete()
    messages.error(request, f'Deleted {model.__class__.__name__}!')
    return redirect(request.GET.get('next', default_redirect))

def str_to_datetime(s: Union[str, None], accept_today: bool=True) -> Union[datetime, None]:
    if accept_today:
        if s == 'today':
            return datetime.now(timezone.utc)
    try:
        return datetime.strptime(s, '%Y-%m-%d')
    except:
        return None