from typing import Any
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest, JsonResponse, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .forms import QuestionAnswerForm, QuestionForm, CompanyForm, VehicleForm
from .models import QuestionAnswerSession, QuestionInstance, QuestionTemplate, Company, QuestionType, Vehicle, add_question_instance_to_session, create_answer_session
from .utils import model_view_create, model_view_update, model_view_delete, str_to_datetime
from datetime import datetime, timedelta, timezone, date



def load_navbar_context(request: HttpRequest) -> dict[str, Any]:
    context = {}
    if request.user.is_authenticated:
        if request.user.profile.position_type == 1 or request.user.profile.position_type == 2:
            context = {
                'base_vehicles': sorted(list(set(Vehicle.objects.filter(questiontemplate__position_type=request.user.profile.position_type).all())), key=lambda v: v.id) # TODO: make this more efficient
            }
        elif request.user.profile.position_type >= 3:
            context = {
                'base_vehicles': Vehicle.objects.all(),
                'base_companies': Company.objects.all()
            }
    return context


def home(request: HttpRequest):
    context = load_navbar_context(request)
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
    context.update(load_navbar_context(request))
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
    context.update(load_navbar_context(request))
    return render(request, 'main/company.html', context=context)


@login_required
@require_http_methods(['GET'])
def delete_company(request: HttpRequest, model_id: int):
    return model_view_delete(request, Company, model_id)


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
    context.update(load_navbar_context(request))
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
    context.update(load_navbar_context(request))
    return render(request, 'main/vehicle.html', context=context)


@login_required
@require_http_methods(['GET', 'POST'])
def delete_vehicle(request: HttpRequest, model_id: int):
    return model_view_delete(request, Vehicle, model_id)


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
    context.update(load_navbar_context(request))
    return render(request, 'main/question_edit.html', context=context)


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
        'set_input_dates_now': False,
        #'url_name': QuestionTemplate.url_name,
        'form': res
    }
    context.update(load_navbar_context(request))
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
    context.update(load_navbar_context(request))
    return render(request, 'main/questions_edit.html', context=context)


@login_required
@require_http_methods(['GET'])
def answers(request: HttpRequest):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    # TODO: apply filters though query parameters
    all_question_intsances = QuestionInstance.objects.filter(answer_session=None)

    question_type = request.GET.get('question_type', None) # may be 0=generic, 1=get on, 2=get off, 3=get on & get off
    if question_type not in [None, '0', '1', '2', '3'] and question_type is not None:
        question_type = None
    if question_type is not None:
        question_type = int(question_type)
    if question_type is not None:
        all_question_intsances = all_question_intsances.filter(question_type=question_type)

    time_to = request.GET.get('time_to', None) # may be today or a date formatted as yyyy-mm-dd
    time_from = request.GET.get('time_from', None) # may be a date formatted as yyyy-mm-dd
    time_to_datetime = str_to_datetime(time_to)
    time_from_datetime = None if time_to == 'today' else str_to_datetime(time_from, False)

    if time_to is None:
        title = 'All Time'
    elif time_to == 'today':
        title = 'Today'
    elif time_from_datetime == None:
        title = time_to_datetime.strftime("%d %b, %Y")
    else:
        title = time_from_datetime.strftime("%d %b, %Y") + ' to ' + time_to_datetime.strftime("%d %b, %Y")

    all_question_intsances = all_question_intsances.order_by('created_at')
    if time_to_datetime:
        start = time_from_datetime if time_from_datetime else datetime(year=time_to_datetime.year, month=time_to_datetime.month, day=time_to_datetime.day)
        answer_instances = all_question_intsances.filter(created_at__range=(start, time_to_datetime)).all()
    else:
        answer_instances = all_question_intsances.all()

    vehicles_ids = set()
    answer_instances_without_vehicle = list()
    for answer_instance in answer_instances:
        if answer_instance.vehicle:
            vehicles_ids.add(answer_instance.vehicle.id)
        else:
            answer_instances_without_vehicle.append(answer_instance)
    answer_instances = {}
    if vehicles_ids:
        vehicles = Vehicle.objects.filter(id__in=vehicles_ids).all()
        for vehicle in vehicles:
            answer_instances[vehicle.name] = vehicle.questioninstance_set.all()
    context = {
        'answer_instances': answer_instances,
        'answer_instances_without_vehicle': answer_instances_without_vehicle,
        'title': title,
        'question_type': question_type,
        'time_to': time_to if time_from_datetime else None,
        'time_from': time_from if time_from_datetime else None
    }
    default_vehicle = request.GET.get('default_vehicle', None)
    if default_vehicle in answer_instances:
        context['default_vehicle'] = default_vehicle
    success_visibility = request.GET.get('success_visibility', None)
    if success_visibility:
        context['success_visibility'] = success_visibility.lower() == 'false'
    accordion_active = request.GET.get('accordion_active', None)
    if accordion_active:
        context['accordion_active'] = accordion_active == 'true'
    context.update(load_navbar_context(request))
    return render(request, 'main/answers.html', context=context)


@login_required
@require_http_methods(['GET'])
def answer(request: HttpRequest, answer_id: int):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    if not QuestionInstance.objects.filter(id=answer_id).exists():
        return HttpResponseNotFound(f'The QuestionInstance with id {answer_id} was not found')
    answer = QuestionInstance.objects.get(id=answer_id)
    form = QuestionAnswerForm(instance=answer, readonly=True)
    context = {
        'form': form
    }
    context.update(load_navbar_context(request))
    return render(request, 'main/answer.html', context=context)



### answer questions

@login_required
@require_http_methods(['GET'])
def questions_answer_portal(request: HttpRequest, vehicle_id: int):
    if request.user.profile.position_type not in (1, 2):
        return HttpResponseForbidden("You can't view this page because you aren't a driver or a mechanic")
    if not Vehicle.objects.filter(id=vehicle_id).exists():
        return HttpResponseBadRequest(f'No vehicle was found with id {vehicle_id}')
    session_types = [t.value for t in QuestionType if QuestionTemplate.objects.filter(vehicles__id=vehicle_id, position_type=request.user.profile.position_type, question_type=t).exists()]
    print(session_types)
    vehicle = Vehicle.objects.get(id=vehicle_id)
    context = {
        'vehicle': vehicle,
        'session_types': session_types
    }
    context.update(load_navbar_context(request))
    return render(request, 'main/question_answer_portal.html', context=context)


@login_required
@require_http_methods(['GET', 'POST'])
def questions_answer_session(request: HttpRequest, vehicle_id: int, session_type: int, page: int=0):
    # answer pagination for a particular vehicle
    if request.user.profile.position_type not in (1, 2):
        return HttpResponseForbidden("You can't view this page because you aren't a driver or a mechanic")
    if not Vehicle.objects.filter(id=vehicle_id).exists():
        return HttpResponseBadRequest(f'No vehicle was found with id {vehicle_id}')
    
    if 'back' in request.GET:
        return redirect('main-answer_session', vehicle_id=vehicle.id, session_type=session_type, page=min(page-1, 0))
    
    
    session_type_cls = QuestionType.get_type_from_int(session_type)

    now_utc = datetime.now(timezone.utc)
    vehicle = Vehicle.objects.get(id=vehicle_id)
    active_session = None
    if QuestionAnswerSession.objects.filter(vehicle=vehicle, user=request.user, session_type=session_type_cls).exists():
        active_session = QuestionAnswerSession.objects.get(vehicle=vehicle, user=request.user, session_type=session_type_cls)
        if now_utc - active_session.created_at > timedelta(minutes=10): # TODO: check if this should be more dynamic. maybe it depends on the session type?
            active_session.questioninstance_set.all().delete()
            active_session.delete()
            messages.info(request, 'Last answer session expired. Starting a new one.')
            active_session = None
    if active_session is None:
        active_session = create_answer_session(request.user, vehicle, session_type_cls, now_utc)
    
    question_templates = list(active_session.questiontemplate_set.order_by('id').all())
    if page >= len(question_templates):
        return HttpResponseBadRequest(f'Page parameter = {page} is to big for number of question templates available = {len(question_templates)}')
    question_template = question_templates[page]
    if active_session.questioninstance_set.filter(question_template=question_template).exists():
        question_instance = active_session.questioninstance_set.get(question_template=question_template)
    else:
        question_instance = add_question_instance_to_session(active_session, question_template)

    context = {
        'vehicle': vehicle,
        'curr_page': page,
        'last_page': len(question_templates)-1,
        'session_type': session_type
    }
    context.update(load_navbar_context(request))
    if request.method == 'POST':
        form = QuestionAnswerForm(request.POST, instance=question_instance)
        context['form'] = form
        if form.is_valid():
            form.save()
            if page < len(question_templates)-1:
                return redirect('main-answer_session', vehicle_id=vehicle.id, session_type=session_type, page=page+1)
            # last page
            active_session.delete()
            messages.success(request, 'You finished an answer session!')
            return redirect(request.GET.get('next', 'main-home'))
    else:
        form = QuestionAnswerForm(instance=question_instance)
        context['form'] = form
    print(form.errors)
    return render(request, 'main/question_answer_session.html', context=context)


### api

# from main.utils import get_all_nonabstract_models_from_module
# api_models = get_all_nonabstract_models_from_module('main.models') | get_all_nonabstract_models_from_module('user.models')

# @login_required
# @require_http_methods(['GET', 'DELETE'])
# def api_single(request: HttpRequest, url_name: str, model_id: id):
#     if request.user.profile.position_type < 3:
#         return HttpResponseForbidden("You haven't got the rank to view this page")
#     if url_name not in api_models:
#         return HttpResponseNotFound('This url does not match to any api path')
#     model_class = api_models[url_name]
#     if not model_class.objects.filter(id=model_id).exists():
#         return HttpResponseNotFound(f'No model instance of "{url_name}" with id "{model_id}" found')
#     model_instance = model_class.objects.get(id=model_id)
#     if request.method == 'GET':
#         return JsonResponse({'id': model_instance.id, 'str': str(model_instance)})
#     elif request.method == 'DELETE':
#         model_instance.delete()
#         return JsonResponse({'status': 'OK', 'message': 'deleted model instance'})
#     elif request.method == 'POST': # TODO: needs type checking!!!
#         for qp_key, qp_value in request.GET.items():
#             if not hasattr(model_instance, qp_key):
#                 return HttpResponseBadRequest(f'Model instance of "{url_name}" has no attribute named "{qp_key}"')
#             setattr(model_instance, qp_key, qp_value)
#         model_instance.save()
#         return JsonResponse({'status': 'OK', 'message': 'saved changes'})
#     return HttpResponseServerError(f'The method "{request.method}" is not supported in this path')

# @login_required
# @require_http_methods(['GET'])
# def api_multiple(request: HttpRequest, url_name: str):
#     if request.user.profile.position_type < 3:
#         return HttpResponseForbidden("You haven't got the rank to view this page")
#     if url_name not in api_models:
#         return HttpResponseNotFound('This url does not match to any api path')
#     model_class = api_models[url_name]
#     if request.method == 'GET':
#         model_instances = model_class.objects.all()
#         return JsonResponse([{'id': m.id, 'str': str(m)} for m in model_instances], safe=False)
#     elif request.method == 'PUT':
#         try:
#             new_model = model_class(**{k:v for k, v in request.GET.items()})
#             new_model.save()
#             return JsonResponse({'status': 'OK', 'message': 'created instance', 'id': new_model.id})
#         except Exception as err:
#             return HttpResponseBadRequest(str(err))
#     return HttpResponseServerError(f'The method "{request.method}" is not supported in this path')


### utils views

def hello_world(request: HttpRequest):
    return HttpResponse('Hello, world!')


def test(request:HttpRequest):
    context = {
        'user_info': True
    }
    context.update(load_navbar_context(request))
    return render(request, 'main/test.html', context=context)
