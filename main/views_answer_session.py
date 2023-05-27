from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest, JsonResponse, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from datetime import datetime, timedelta, timezone

from .utils import redirect_params, dict_get
from .forms import QuestionAnswerForm
from .models import AnswerSession, QuestionInstance, QuestionTemplate, QuestionType, Vehicle, add_question_instance_to_session, create_answer_session
from user.models import Profile



def _bad_user_message():
    return f"You can't view this page because you are not don't have one of the following user positions: {', '.join([pos.label for pos in Profile.PositionType])}"


@login_required
@require_http_methods(['GET'])
def questions_answer_portal(request: HttpRequest, vehicle_id: int):
    if request.user.profile.position_type not in (1, 2):
        return HttpResponseForbidden(_bad_user_message())
    if not Vehicle.objects.filter(id=vehicle_id).exists():
        return HttpResponseBadRequest(f'No vehicle was found with id {vehicle_id}')
    session_types = QuestionTemplate.objects.filter(vehicles__id=vehicle_id, position_type=request.user.profile.position_type).values('question_types').distinct().values_list('question_types__id', 'question_types__name')
    vehicle = Vehicle.objects.get(id=vehicle_id)
    context = {
        'vehicle': vehicle,
        'session_types': session_types
    }
    return render(request, 'main/question_answer_portal.html', context=context)


@login_required
@require_http_methods(['GET', 'POST'])
def questions_answer_session(request: HttpRequest, vehicle_id: int, question_type_id: int):
    # page is 1 over the corresponding question_template index of the answer_session
    SESSION_EXPIRATION_TIME = timedelta(minutes=10)
    # answer pagination for a particular vehicle
    if request.user.profile.position_type not in (1, 2):
        return HttpResponseForbidden(_bad_user_message())
    if not Vehicle.objects.filter(id=vehicle_id).exists():
        return HttpResponseBadRequest(f'No vehicle was found with id {vehicle_id}')
    if not QuestionType.objects.filter(id=question_type_id).exists():
        return HttpResponseBadRequest(f'No vehicle was found with id {vehicle_id}')
    
    now_utc = datetime.now(timezone.utc)
    vehicle = Vehicle.objects.get(id=vehicle_id)
    question_type = QuestionType.objects.get(id=question_type_id)
    active_session = None
    if AnswerSession.objects.filter(user=request.user, vehicle=vehicle, question_type=question_type, complete=False).exists():
        active_session = AnswerSession.objects.get(user=request.user, vehicle=vehicle, question_type=question_type, complete=False)
        if now_utc - active_session.created_at > SESSION_EXPIRATION_TIME:
            active_session.delete()
            active_session = None
    if active_session is None:
        active_session = create_answer_session(request.user, vehicle, question_type)
    
    question_templates = list(active_session.question_templates.order_by('id').all())
    get_dict = request.GET
    page = dict_get(get_dict, 'page', -1, int)
    if page == -1: # get first non-completed question
        if active_session.question_instances.all().exists():
            for qt_idx in range(len(question_templates)):
                if not active_session.question_instances.filter(question_template=question_templates[qt_idx]).exists():
                    page = qt_idx
                    print(page)
                    break
        page = page if page != -1 else 0
    if page >= len(question_templates) or page < 0:
        return HttpResponseBadRequest(f'Page index parameter (= {page}) is to big for number of question templates available (= {len(question_templates)})')
    question_template = question_templates[page]
    if QuestionInstance.objects.filter(answer_session=active_session, question_template=question_template).exists():
        question_instance = QuestionInstance.objects.get(answer_session=active_session, question_template=question_template)
    else:
        question_instance = add_question_instance_to_session(active_session, question_template)

    context = {
        'vehicle': vehicle,
        'curr_page': page,
        'last_page': len(question_templates)-1,
        'question_type': question_type
    }
    if request.method == 'POST':
        next_page = dict_get(get_dict, 'next_page', page+1, int)
        form = QuestionAnswerForm(request.POST, instance=question_instance)
        context['form'] = form
        if form.is_valid():
            form.save()
            if page < len(question_templates)-1:
                return redirect_params('main-answer_session', vehicle_id=vehicle.id, question_type_id=question_type.id, params={'page': next_page})
                return redirect('main-answer_session', vehicle_id=vehicle.id, question_type_id=question_type.id) # SET QUERY PARAMS
            # last page
            active_session.complete = True
            active_session.save()
            messages.success(request, 'You finished an answer session!')
            return redirect(request.GET.get('next', 'main-home'))
    else:
        form = QuestionAnswerForm(instance=question_instance)
        context['form'] = form
    return render(request, 'main/question_answer_session.html', context=context)
