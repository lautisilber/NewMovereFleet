from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest, JsonResponse, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .forms import QuestionAnswerForm, QuestionForm, CompanyForm, VehicleForm
from .models import QuestionInstance, QuestionTemplate, Company, Vehicle, create_question_instance
from .utils import model_view_create, model_view_update, model_view_delete
from datetime import datetime, timezone


def home(request: HttpRequest):
    context = {}
    if request.user.is_authenticated:
        if request.user.profile.position_type == 1 or request.user.profile.position_type == 2:
            context = {
                'vehicles': Vehicle.objects.all()
            }
    return render(request, 'main/home.html', context=context)


### company

@login_required
@require_http_methods(['GET', 'POST'])
def create_company(request: HttpRequest):
    res = model_view_create(request, CompanyForm)

    if isinstance(res, HttpResponse):
        return res

    context = {
        'title': 'Create Company',
        'ok_button_text': 'Create',
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
        'title': 'Update Company',
        'ok_button_text': 'Update',
        'model': res.instance,
        'form': res
    }
    return render(request, 'main/company.html', context=context)


@login_required
@require_http_methods(['GET'])
def delete_company(request: HttpRequest, model_id: int):
    return model_view_delete(request, Company, model_id)


@login_required
@require_http_methods(['GET'])
def companies(request: HttpRequest):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    context = {
        'models': Company.objects.all()
    }
    return render(request, 'main/companies.html', context=context)


### vehicles

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


@login_required
@require_http_methods(['GET'])
def vehicles(request: HttpRequest):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    context = {
        'models': Vehicle.objects.all()
    }
    return render(request, 'main/vehicles.html', context=context)


### questions

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
    return render(request, 'main/question.html', context=context)


@login_required
@require_http_methods(['GET', 'POST'])
def update_question(request: HttpRequest, model_id: int):
    res = model_view_update(request, QuestionForm, model_id)

    if isinstance(res, HttpResponse):
        return res

    context = {
        'title': 'Update Question',
        'ok_button_text': 'Update',
        'model': res.instance,
        'set_input_dates_now': True,
        #'url_name': QuestionTemplate.url_name,
        'form': res
    }
    return render(request, 'main/question.html', context=context)


@login_required
@require_http_methods(['GET', 'POST'])
def delete_question(request: HttpRequest, model_id: int):
    return model_view_delete(request, QuestionTemplate, model_id)


@login_required
@require_http_methods(['GET'])
def questions(request: HttpRequest):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    context = {
        'models': QuestionTemplate.objects.all()
    }
    return render(request, 'main/questions.html', context=context)


### answer questions

@login_required
@require_http_methods(['GET'])
def questions_answer(request: HttpRequest):
    if request.user.profile.position_type not in (1, 2):
        return HttpResponseForbidden("You can't view this page because you aren't a driver or a mechanic")
    vehicle_id = None
    if 'vehicle_id' in request.GET:
        vehicle_id = [request.GET['vehicle_id']]
    elif 'vehicle_id[]' in request.GET:
        vehicle_id = request.GET.getlist('vehicle_id[]')
    if vehicle_id is None:
        vehicles = Vehicle.objects.all()
    else:
        if not all(p.isdigit() for p in vehicle_id):
            return HttpResponseBadRequest('Not all vehicle ids were integers')
        vehicles = Vehicle.objects.filter(id__in=vehicle_id)

    questions = {}
    for vehicle in vehicles:
        # https://stackoverflow.com/questions/2218327/django-manytomany-filter
        pos_type_questions = QuestionTemplate.objects.filter(position_type=request.user.profile.position_type)
        now_utc = datetime.now(timezone.utc)
        if QuestionTemplate.objects.filter(vehicles=vehicle).exists():
            questions[vehicle.id] = [(question, question.should_be_instantiated(now_utc=now_utc)[0]) for question in pos_type_questions.filter(vehicles__id=vehicle.id).all()]
    
    context = {
        'vehicles': vehicles,
        'questions': questions
    }

    print(vehicles)
    print(questions)

    return render(request, 'main/questions_answer.html', context=context)


@login_required
@require_http_methods(['GET', 'POST'])
def question_answer(request: HttpRequest, question_template_id: int):
    if request.user.profile.position_type not in (1, 2):
        return HttpResponseForbidden("You can't view this page because you aren't a driver or a mechanic")
    now_utc = datetime.now(timezone.utc)
    pos_type_questions = QuestionTemplate.objects.filter(position_type=request.user.profile.position_type)
    answerable_questions = [question for question in pos_type_questions if question.should_be_instantiated(now_utc)[0]]
    if not any(question.id == question_template_id for question in answerable_questions):
        return HttpResponseNotFound(f'No answerable question exists with the id {question_template_id}')
    question_template = next(question for question in answerable_questions if question.id == question_template_id)
    print(question_template, type(question_template), question_template.id)
    question_instance = create_question_instance(quesiton_template=question_template, user=request.user)

    if request.method == 'POST':
        form = QuestionAnswerForm(request.POST, instance=question_instance)
        if form.is_valid():
            form.save()
            messages.success(request, f'Answered question {question_template.question}!')
            return redirect(request.GET.get('next', 'main-home'))
    else:
        form = QuestionAnswerForm(instance=question_instance)
    
    context = {
        'form': form
    }
    return render(request, 'main/question_answer.html', context=context)
    

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
