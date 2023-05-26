from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest, JsonResponse, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .utils import model_view_create, model_view_update, model_view_delete
from .forms import QuestionForm
from .models import QuestionTemplate, QuestionType



@login_required
@require_http_methods(['GET', 'POST'])
def create_question(request: HttpRequest):
    res = model_view_create(request, QuestionForm)

    if isinstance(res, HttpResponse):
        return res

    context = {
        'title': 'Create Question',
        'ok_button_text': 'Create',
        'set_input_dates_now': True,
        'form': res
    }
    print(any(e[0] for e in res.instance.question_tepmlate.question_types.values_list('periodicity')))
    return render(request, 'main/question_edit.html', context=context)


@login_required
@require_http_methods(['GET', 'POST'])
def update_question(request: HttpRequest, model_id: int):
    res = model_view_update(request, QuestionForm, model_id)

    if isinstance(res, HttpResponse):
        return res

    periodicities = {t.id:t.periodicity for t in QuestionType.objects.all()}
    context = {
        'title': 'Update Question',
        'ok_button_text': 'Update',
        'model': res.instance,
        'set_input_dates_now': False,
        #'url_name': QuestionTemplate.url_name,
        'form': res,
        #'periodicity': any(e[0] for e in res.instance.question_types.values_list('periodicity'))
        'periodicities': periodicities
    }
    return render(request, 'main/question_edit.html', context=context)


@login_required
@require_http_methods(['GET', 'POST'])
def delete_question(request: HttpRequest, model_id: int):
    return model_view_delete(request, QuestionTemplate, model_id)


@login_required
@require_http_methods(['GET'])
def questions(request: HttpRequest):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    question_templates = QuestionTemplate.objects.all()
    vehicles = {question_template.id:list(question_template.vehicles.all()) for question_template in question_templates}
    context = {
        'question_templates': question_templates,
        'vehicles': vehicles
    }
    return render(request, 'main/questions_edit.html', context=context)