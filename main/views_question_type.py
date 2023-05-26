from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest, JsonResponse, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .utils import model_view_create, model_view_update, model_view_delete
from .forms import QuestionTypeForm
from .models import QuestionType


@login_required
@require_http_methods(['GET', 'POST'])
def create_question_type(request: HttpRequest):
    res = model_view_create(request, QuestionTypeForm)

    if isinstance(res, HttpResponse):
        return res

    context = {
        'title': 'Create Question Type',
        'ok_button_text': 'Create',
        'form': res
    }
    return render(request, 'main/question_type.html', context=context)


@login_required
@require_http_methods(['GET', 'POST'])
def update_question_type(request: HttpRequest, model_id: int):
    res = model_view_update(request, QuestionTypeForm, model_id)

    if isinstance(res, HttpResponse):
        return res

    context = {
        'title': 'Update Question Type',
        'ok_button_text': 'Update',
        'model': res.instance,
        'form': res
    }
    return render(request, 'main/question_type.html', context=context)


@login_required
@require_http_methods(['GET', 'POST'])
def delete_question_type(request: HttpRequest, model_id: int):
    return model_view_delete(request, QuestionType, model_id)