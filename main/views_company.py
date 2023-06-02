from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest, JsonResponse, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .utils import model_view_create, model_view_update, model_view_delete
from .forms import CompanyForm
from .models import Company


@login_required
@require_http_methods(['GET', 'POST'])
def create_company(request: HttpRequest):
    res = model_view_create(request, CompanyForm)

    if isinstance(res, HttpResponse):
        return res

    context = {
        'title': 'Crear Company',
        'ok_button_text': 'Crear',
        'form': res
    }
    return render(request, 'main/company.html', context=context)


@login_required
@require_http_methods(['GET', 'POST'])
def update_company(request: HttpRequest, model_id: int):
    res = model_view_update(request, CompanyForm, model_id)

    if isinstance(res, HttpResponse):
        return res

    context = {
        'title': 'Editar Company',
        'ok_button_text': 'Confirmar edición',
        'model': res.instance,
        'form': res
    }
    return render(request, 'main/company.html', context=context)


@login_required
@require_http_methods(['GET'])
def delete_company(request: HttpRequest, model_id: int):
    return model_view_delete(request, Company, model_id)