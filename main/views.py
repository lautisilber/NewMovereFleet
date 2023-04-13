from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest, JsonResponse, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .forms import ChecklistForm, ChecklistQuestionForm, CompanyForm
from .models import ChecklistQuestionTemplate, ChecklistTemplate, Company


def home(request: HttpRequest):
    return render(request, 'main/home.html')


### company

@login_required
def create_company(request: HttpRequest):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    if request.method == 'POST':
        form = Company(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Created company {form.instance.name}!')
            return redirect(request.GET.get('next', 'main-home'))
    else:
        form = Company()
    context = {
        'form': form,
        'ok_button_text': 'Create'
    }
    return render(request, 'main/company.html', context=context)


@login_required
def update_checklist(request: HttpRequest, company_id: int):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    if not Company.objects.filter(id=company_id).exists():
        return HttpResponseNotFound(f'The checklist template with id {company_id} was not found')
    company = Company.objects.get(id=company_id)
    if request.method == 'POST':
        form = ChecklistForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, f'Created template checklist {form.instance.name}!')
            return redirect(request.GET.get('next', 'main-home'))
    else:
        form = ChecklistForm(instance=company)
    questions = ChecklistQuestionTemplate.objects.all()
    context = {
        'form': form,
        'questions': questions,
        'checklist': checklist,
        'ok_button_text': 'Update'
    }
    return render(request, 'main/company.html', context=context)


@login_required
def delete_checklist(request: HttpRequest, checklist_id: int):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    if not ChecklistTemplate.objects.filter(id=checklist_id).exists():
        return HttpResponseNotFound(f'The checklist template with id {checklist_id} was not found')
    checklist = ChecklistTemplate.objects.get(id=checklist_id)
    checklist.delete()
    return redirect(request.GET.get('next', 'main-home'))


@login_required
def checklists(request: HttpRequest):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    context = {
        'checklists': ChecklistTemplate.objects.all()
    }
    return render(request, 'main/companies.html', context=context)


### checklists

@login_required
def create_checklist(request: HttpRequest):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    if request.method == 'POST':
        form = ChecklistForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Created template checklist {form.instance.name}!')
            return redirect(request.GET.get('next', 'main-home'))
    else:
        form = ChecklistForm()
    questions = ChecklistQuestionTemplate.objects.all()
    context = {
        'form': form,
        'questions': questions,
        'ok_button_text': 'Create'
    }
    return render(request, 'main/checklist.html', context=context)


@login_required
def update_checklist(request: HttpRequest, checklist_id: int):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    if not ChecklistTemplate.objects.filter(id=checklist_id).exists():
        return HttpResponseNotFound(f'The checklist template with id {checklist_id} was not found')
    checklist = ChecklistTemplate.objects.get(id=checklist_id)
    if request.method == 'POST':
        form = ChecklistForm(request.POST, instance=checklist)
        if form.is_valid():
            form.save()
            messages.success(request, f'Created template checklist {form.instance.name}!')
            return redirect(request.GET.get('next', 'main-home'))
    else:
        form = ChecklistForm(instance=checklist)
    questions = ChecklistQuestionTemplate.objects.all()

    # HEY. maybe this is a way to acces individual fields from forms in the template
    # form.fields['template'].initial = True

    context = {
        'form': form,
        'questions': questions,
        'checklist': checklist,
        'ok_button_text': 'Update'
    }
    return render(request, 'main/checklist.html', context=context)


@login_required
def delete_checklist(request: HttpRequest, checklist_id: int):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    if not ChecklistTemplate.objects.filter(id=checklist_id).exists():
        return HttpResponseNotFound(f'The checklist template with id {checklist_id} was not found')
    checklist = ChecklistTemplate.objects.get(id=checklist_id)
    checklist.delete()
    return redirect(request.GET.get('next', 'main-home'))


@login_required
def checklists(request: HttpRequest):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    context = {
        'checklists': ChecklistTemplate.objects.all()
    }
    return render(request, 'main/checklists.html', context=context)


### checklist questions

@login_required
def create_question(request: HttpRequest):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    if request.method == 'POST':
        form = ChecklistQuestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Created checklist question checklist titled {form.instance.title}!')
            return redirect(request.GET.get('next', 'main-home'))
    else:
        form = ChecklistQuestionForm()

    context = {
        'title': 'Create Question',
        'ok_button_text': 'Create',
        'form': form
    }
    return render(request, 'main/question.html', context=context)


@login_required
def update_question(request: HttpRequest, question_id: int):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    if not ChecklistQuestionTemplate.objects.filter(id=question_id).exists():
        return HttpResponseNotFound(f'The question template with id {question_id} was not found')
    question = ChecklistQuestionTemplate.objects.get(id=question_id)
    if request.method == 'POST':
        form = ChecklistQuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, f'Created checklist question checklist titled {form.instance.title}!')
            return redirect(request.GET.get('next', 'main-home'))
    else:
        form = ChecklistQuestionForm(instance=question)

    context = {
        'title': 'Update Question',
        'ok_button_text': 'Update',
        'question': question,
        #'url_name': ChecklistQuestionTemplate.url_name,
        'form': form
    }
    return render(request, 'main/question.html', context=context)


@login_required
def delete_question(request: HttpRequest, question_id: int):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    if not ChecklistQuestionTemplate.objects.filter(id=question_id).exists():
        return HttpResponseNotFound(f'The form question template with id {question_id} was not found')
    question = ChecklistQuestionTemplate.objects.get(id=question_id)
    question.delete()
    return redirect(request.GET.get('next', 'main-home'))


@login_required
def questions(request: HttpRequest):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    context = {
        'questions': ChecklistQuestionTemplate.objects.all()
    }
    return render(request, 'main/questions.html', context=context)


### api
from main.utils import get_all_nonabstract_models_from_module
api_models = get_all_nonabstract_models_from_module('main.models') | get_all_nonabstract_models_from_module('user.models')

@login_required
@require_http_methods(['GET', 'DELETE'])
def api_single(request: HttpRequest, url_name: str, model_id: id):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    if url_name not in api_models:
        return HttpResponseNotFound('This url does not match to any api path')
    model_class = api_models[url_name]
    if not model_class.objects.filter(id=model_id).exists():
        return HttpResponseNotFound(f'No model instance of "{url_name}" with id "{model_id}" found')
    model_instance = model_class.objects.get(id=model_id)
    if request.method == 'GET':
        return JsonResponse({'id': model_instance.id, 'str': str(model_instance)})
    elif request.method == 'DELETE':
        model_instance.delete()
        return JsonResponse({'status': 'OK', 'message': 'deleted model instance'})
    elif request.method == 'POST': # TODO: needs type checking!!!
        for qp_key, qp_value in request.GET.items():
            if not hasattr(model_instance, qp_key):
                return HttpResponseBadRequest(f'Model instance of "{url_name}" has no attribute named "{qp_key}"')
            setattr(model_instance, qp_key, qp_value)
        model_instance.save()
        return JsonResponse({'status': 'OK', 'message': 'saved changes'})
    return HttpResponseServerError(f'The method "{request.method}" is not supported in this path')

@login_required
@require_http_methods(['GET'])
def api_multiple(request: HttpRequest, url_name: str):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    if url_name not in api_models:
        return HttpResponseNotFound('This url does not match to any api path')
    model_class = api_models[url_name]
    if request.method == 'GET':
        model_instances = model_class.objects.all()
        return JsonResponse([{'id': m.id, 'str': str(m)} for m in model_instances], safe=False)
    elif request.method == 'PUT':
        try:
            new_model = model_class(**{k:v for k, v in request.GET.items()})
            new_model.save()
            return JsonResponse({'status': 'OK', 'message': 'created instance', 'id': new_model.id})
        except Exception as err:
            return HttpResponseBadRequest(str(err))
    return HttpResponseServerError(f'The method "{request.method}" is not supported in this path')


### utils views

def hello_world(request: HttpRequest):
    return HttpResponse('Hello, world!')


def test(request:HttpRequest):
    context = {
        'user_info': True
    }
    return render(request, 'main/test.html', context=context)
