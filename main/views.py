from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden, HttpResponseNotFound
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
            messages.success(request, f'Created checklist question checklist titled {form.data["title"]}!')
            return redirect(request.GET.get('next', 'main-home'))
    else:
        form = ChecklistQuestionCreateForm()

    context = {
        'title': 'Create Question',
        'form': form
    }
    return render(request, 'main/question.html', context=context)


@login_required
def update_question(request: HttpRequest, question_id: int):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    question = ChecklistQuestionTemplate.objects.get(id=question_id)
    if not question:
        return HttpResponseNotFound(f'The form question template with id {question_id} was not found')
    if request.method == 'POST':
        form = ChecklistQuestionCreateForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, f'Created checklist question checklist titled {form.data["title"]}!')
            return redirect(request.GET.get('next', 'main-home'))
    else:
        form = ChecklistQuestionCreateForm(instance=question)

    context = {
        'title': 'Update Question',
        'form': form
    }
    return render(request, 'main/question.html', context=context)

@login_required
def questions(request: HttpRequest):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    context = {
        'questions': ChecklistQuestionTemplate.objects.all()
    }
    return render(request, 'main/questions.html', context=context)
    

### utils views

def hello_world(request: HttpRequest):
    return HttpResponse('Hello, world!')


def test(request:HttpRequest):
    context = {
        'user_info': True
    }
    return render(request, 'main/test.html', context=context)
