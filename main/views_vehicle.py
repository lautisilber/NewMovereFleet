from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest, JsonResponse, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .utils import model_view_create, model_view_update, model_view_delete
from .forms import VehicleForm
from .models import Vehicle



@login_required
@require_http_methods(['GET', 'POST'])
def create_vehicle(request: HttpRequest):
    res = model_view_create(request, VehicleForm)

    if isinstance(res, HttpResponse):
        return res

    context = {
        'title': 'Create Vehicle',
        'ok_button_text': 'Create',
        'form': res
    }
    return render(request, 'main/vehicle.html', context=context)


@login_required
@require_http_methods(['GET', 'POST'])
def update_vehicle(request: HttpRequest, model_id: int):
    res = model_view_update(request, VehicleForm, model_id)

    if isinstance(res, HttpResponse):
        return res

    context = {
        'title': 'Update Vehicle',
        'ok_button_text': 'Update',
        'model': res.instance,
        'form': res
    }
    return render(request, 'main/vehicle.html', context=context)


@login_required
@require_http_methods(['GET', 'POST'])
def delete_vehicle(request: HttpRequest, model_id: int):
    return model_view_delete(request, Vehicle, model_id)