from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest, JsonResponse, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from datetime import datetime

from .utils import str_to_datetime
from .forms import QuestionAnswerForm
from .models import QuestionInstance, QuestionType, Vehicle



# @login_required
# @require_http_methods(['GET'])
# def answers(request: HttpRequest):
#     if request.user.profile.position_type < 3:
#         return HttpResponseForbidden("You haven't got the rank to view this page")
#     # TODO: apply filters though query parameters (?)
#     question_instances = QuestionInstance.objects.filter(answer_session=None).order_by('-created_at').all()

#     vehicles_ids = set()
#     question_instances_without_vehicle = list()
#     for question_intsance in question_instances:
#         if question_intsance.vehicle:
#             vehicles_ids.add(question_intsance.vehicle.id)
#         else:
#             question_instances_without_vehicle.append(question_intsance)
#     question_instances = {}
#     if vehicles_ids:
#         vehicles = Vehicle.objects.filter(id__in=vehicles_ids).all()
#         for vehicle in vehicles:
#             question_instances[vehicle.name] = vehicle.question_instances.all()
#     context = {
#         'answer_instances': question_instances,
#         'answer_instances_without_vehicle': question_instances_without_vehicle,
#         'title': 'Answers',
#         'question_types': QuestionType.objects.all(),
#         'all_vehicles': Vehicle.objects.all()
#     }
#     return render(request, 'main/answers.html', context=context)


@login_required
@require_http_methods(['GET'])
def answers(request: HttpRequest):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    # TODO: apply filters though query parameters (?)
    question_instances = {}
    vehicles = Vehicle.objects.all()
    for vehicle in vehicles:
        question_instances[vehicle.name] = vehicle.question_instances.filter(answer_session__complete=True).order_by('-created_at').all()
    print(question_instances)
    context = {
        'answer_instances': question_instances,
        'title': 'Answers',
        'question_types': QuestionType.objects.all(),
        'all_vehicles': Vehicle.objects.all()
    }
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
    return render(request, 'main/answer.html', context=context)




# @login_required
# @require_http_methods(['GET'])
# def answers(request: HttpRequest):
#     if request.user.profile.position_type < 3:
#         return HttpResponseForbidden("You haven't got the rank to view this page")
#     # TODO: apply filters though query parameters
#     all_question_instances = QuestionInstance.objects.filter(answer_session=None)

#     question_type = request.GET.get('question_type', None) # may be 0=generic, 1=get on, 2=get off, 3=get on & get off
#     if question_type not in [None, '0', '1', '2', '3'] and question_type is not None:
#         question_type = None
#     if question_type is not None:
#         question_type = int(question_type)
#     if question_type is not None:
#         all_question_instances = all_question_instances.filter(question_type=question_type)

#     time_to = request.GET.get('time_to', None) # may be today or a date formatted as yyyy-mm-dd
#     time_from = request.GET.get('time_from', None) # may be a date formatted as yyyy-mm-dd
#     time_to_datetime = str_to_datetime(time_to)
#     time_from_datetime = None if time_to == 'today' else str_to_datetime(time_from, False)

#     if time_to is None:
#         title = 'All Time'
#     elif time_to == 'today':
#         title = 'Today'
#     elif time_from_datetime == None:
#         title = time_to_datetime.strftime("%d %b, %Y")
#     else:
#         title = time_from_datetime.strftime("%d %b, %Y") + ' to ' + time_to_datetime.strftime("%d %b, %Y")

#     all_question_instances = all_question_instances.order_by('created_at')
#     if time_to_datetime:
#         start = time_from_datetime if time_from_datetime else datetime(year=time_to_datetime.year, month=time_to_datetime.month, day=time_to_datetime.day)
#         answer_instances = all_question_instances.filter(created_at__range=(start, time_to_datetime)).all()
#     else:
#         answer_instances = all_question_instances.all()

#     vehicles_ids = set()
#     answer_instances_without_vehicle = list()
#     for answer_instance in answer_instances:
#         if answer_instance.vehicle:
#             vehicles_ids.add(answer_instance.vehicle.id)
#         else:
#             answer_instances_without_vehicle.append(answer_instance)
#     answer_instances = {}
#     if vehicles_ids:
#         vehicles = Vehicle.objects.filter(id__in=vehicles_ids).all()
#         for vehicle in vehicles:
#             answer_instances[vehicle.name] = vehicle.questioninstance_set.all()
#     context = {
#         'answer_instances': answer_instances,
#         'answer_instances_without_vehicle': answer_instances_without_vehicle,
#         'title': title,
#         'question_type': question_type,
#         'time_to': time_to if time_from_datetime else None,
#         'time_from': time_from if time_from_datetime else None
#     }
#     default_vehicle = request.GET.get('default_vehicle', None)
#     if default_vehicle in answer_instances:
#         context['default_vehicle'] = default_vehicle
#     success_visibility = request.GET.get('success_visibility', None)
#     if success_visibility:
#         context['success_visibility'] = success_visibility.lower() == 'false'
#     accordion_active = request.GET.get('accordion_active', None)
#     if accordion_active:
#         context['accordion_active'] = accordion_active == 'true'
#     return render(request, 'main/answers.html', context=context)