from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest, JsonResponse, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .forms import QuestionForm, CompanyForm, VehicleForm
from .models import QuestionTemplate, Company, Vehicle
from .utils import model_view_create, model_view_update, model_view_delete
from datetime import datetime, timezone


def home(request: HttpRequest):
    context = {}
    if request.user.profile.position_type == 1 or request.user.profile.position_type == 2:
        context = {
            'vehicles': Vehicle.objects.all()
        }
    return render(request, 'main/home.html', context=context)


### company

@login_required
@require_http_methods(['GET'])
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
@require_http_methods(['GET'])
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
@require_http_methods(['GET'])
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
@require_http_methods(['GET'])
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
@require_http_methods(['GET'])
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
@require_http_methods(['GET'])
def create_question(request: HttpRequest):
    res = model_view_create(request, QuestionForm)

    if isinstance(res, HttpResponse):
        return res

    context = {
        'title': 'Create Question',
        'ok_button_text': 'Create',
        'form': res
    }
    return render(request, 'main/question.html', context=context)


@login_required
@require_http_methods(['GET'])
def update_question(request: HttpRequest, model_id: int):
    res = model_view_update(request, QuestionForm, model_id)

    if isinstance(res, HttpResponse):
        return res

    context = {
        'title': 'Update Question',
        'ok_button_text': 'Update',
        'model': res.instance,
        #'url_name': QuestionTemplate.url_name,
        'form': res
    }
    return render(request, 'main/question.html', context=context)


@login_required
@require_http_methods(['GET'])
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


### answer questions

@login_required
@require_http_methods(['GET'])
def questions_answer(request: HttpRequest):
    vehicle_ids = request.GET.get('vehicle_ids', None)
    if vehicle_ids is None:
        vehicles = Vehicle.objects.all()
    elif isinstance(vehicle_ids, int):
        if not Vehicle.objects.filter(id=vehicle_ids).exists():
            return HttpResponseNotFound(f'No vehicle found with id = {vehicle_ids}')
        vehicles = [Vehicle.objects.get(id=vehicle_ids)]
    elif isinstance(vehicle_ids, list):
        if not Vehicle.objects.filter(id__in=vehicle_ids).exists():
            return HttpResponseNotFound(f'No vehicle found with ids = {vehicle_ids}')
        vehicles = Vehicle.objects.get(id__in=vehicle_ids)

    questions = {}
    for vehicle in vehicles:
        # https://stackoverflow.com/questions/2218327/django-manytomany-filter
        pos_type_questions = QuestionTemplate.objects.filter(position_type=request.user.profile.position_type)
        if QuestionTemplate.objects.filter(vehicles=vehicle).exists():
            questions[vehicle.id] = [(question, question.should_be_instantiated(now_utc=datetime.now(timezone=timezone.utc)[0])) for question in pos_type_questions.filter(vehicles__id=vehicle.id).all()]
    
    context = {
        'vehicles': vehicles,
        'questions': questions
    }

    return render(request, 'main/questions_answer_list', context=context)




### utils views

def hello_world(request: HttpRequest):
    return HttpResponse('Hello, world!')


def test(request:HttpRequest):
    context = {
        'user_info': True
    }
    return render(request, 'main/test.html', context=context)
