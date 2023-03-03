from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ChecklistCreateForm, ChecklistQuestionCreateForm
from .models import ChecklistQuestionTemplate


def home(request: HttpRequest):
    return render(request, 'main/home.html')


@login_required
def create_checklist(request: HttpRequest):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    if request.method == 'POST':
        form = ChecklistCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(f'Created template checklist {form.name}!')
            return redirect('main-home')
    else:
        form = ChecklistCreateForm()
    questions = ChecklistQuestionTemplate.objects.all()

    # HEY. maybe this is a way to acces individual fields from forms in the template
    # form.fields['template'].initial = True

    context = {
        'form': form,
        'questions': questions
    }
    return render(request, 'main/create_checklist.html', context=context)


@login_required
def create_question(request: HttpRequest):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    if request.method == 'POST':
        form = ChecklistQuestionCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(f'Created checklist question checklist titled {form.title}!')
            return redirect('main-home')
    else:
        form = ChecklistQuestionCreateForm()

    context = {
        'form': form
    }
    return render(request, 'main/create_question.html', context=context)


### utils views

def hello_world(request: HttpRequest):
    return HttpResponse('Hello, world!')


def test(request:HttpRequest):
    context = {
        'user_info': True
    }
    return render(request, 'main/test.html', context=context)
