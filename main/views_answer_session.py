from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest, JsonResponse, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from datetime import datetime

from .utils import str_to_datetime
from .forms import QuestionAnswerForm
from .models import QuestionInstance, Vehicle



@login_required
@require_http_methods(['GET'])
def questions_answer_portal(request: HttpRequest, vehicle_id: int):
    # if request.user.profile.position_type not in (1, 2):
    #     return HttpResponseForbidden("You can't view this page because you aren't a driver or a mechanic")
    # if not Vehicle.objects.filter(id=vehicle_id).exists():
    #     return HttpResponseBadRequest(f'No vehicle was found with id {vehicle_id}')
    # session_types = [t.value for t in QuestionType if QuestionTemplate.objects.filter(vehicles__id=vehicle_id, position_type=request.user.profile.position_type, question_type=t).exists()]
    # print(session_types)
    # vehicle = Vehicle.objects.get(id=vehicle_id)
    # context = {
    #     'vehicle': vehicle,
    #     'session_types': session_types
    # }
    # context.update(load_navbar_context(request))
    # return render(request, 'main/question_answer_portal.html', context=context)
    return redirect('main-home')


@login_required
@require_http_methods(['GET', 'POST'])
def questions_answer_session(request: HttpRequest, vehicle_id: int, session_type: int, page: int=0):
    # # answer pagination for a particular vehicle
    # if request.user.profile.position_type not in (1, 2):
    #     return HttpResponseForbidden("You can't view this page because you aren't a driver or a mechanic")
    # if not Vehicle.objects.filter(id=vehicle_id).exists():
    #     return HttpResponseBadRequest(f'No vehicle was found with id {vehicle_id}')
    
    # if 'back' in request.GET:
    #     return redirect('main-answer_session', vehicle_id=vehicle.id, session_type=session_type, page=min(page-1, 0))
    
    
    # session_type_cls = QuestionType.get_type_from_int(session_type)

    # now_utc = datetime.now(timezone.utc)
    # vehicle = Vehicle.objects.get(id=vehicle_id)
    # active_session = None
    # if QuestionAnswerSession.objects.filter(vehicle=vehicle, user=request.user, session_type=session_type_cls).exists():
    #     active_session = QuestionAnswerSession.objects.get(vehicle=vehicle, user=request.user, session_type=session_type_cls)
    #     if now_utc - active_session.created_at > timedelta(minutes=10): # TODO: check if this should be more dynamic. maybe it depends on the session type?
    #         active_session.questioninstance_set.all().delete()
    #         active_session.delete()
    #         messages.info(request, 'Last answer session expired. Starting a new one.')
    #         active_session = None
    # if active_session is None:
    #     active_session = create_answer_session(request.user, vehicle, session_type_cls, now_utc)
    
    # question_templates = list(active_session.questiontemplate_set.order_by('id').all())
    # if page >= len(question_templates):
    #     return HttpResponseBadRequest(f'Page parameter = {page} is to big for number of question templates available = {len(question_templates)}')
    # question_template = question_templates[page]
    # if active_session.questioninstance_set.filter(question_template=question_template).exists():
    #     question_instance = active_session.questioninstance_set.get(question_template=question_template)
    # else:
    #     question_instance = add_question_instance_to_session(active_session, question_template)

    # context = {
    #     'vehicle': vehicle,
    #     'curr_page': page,
    #     'last_page': len(question_templates)-1,
    #     'session_type': session_type
    # }
    # context.update(load_navbar_context(request))
    # if request.method == 'POST':
    #     form = QuestionAnswerForm(request.POST, instance=question_instance)
    #     context['form'] = form
    #     if form.is_valid():
    #         form.save()
    #         if page < len(question_templates)-1:
    #             return redirect('main-answer_session', vehicle_id=vehicle.id, session_type=session_type, page=page+1)
    #         # last page
    #         active_session.delete()
    #         messages.success(request, 'You finished an answer session!')
    #         return redirect(request.GET.get('next', 'main-home'))
    # else:
    #     form = QuestionAnswerForm(instance=question_instance)
    #     context['form'] = form
    # print(form.errors)
    # return render(request, 'main/question_answer_session.html', context=context)
    return redirect('main-home')