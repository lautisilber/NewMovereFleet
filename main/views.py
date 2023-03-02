from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .forms import ChecklistCreateForm, ChecklistQuestionCreateForm
from .models import ChecklistQuestion


# The frontend works as follows 
# There is a base html with all the required CDNs. It also has some templating to add 
# commonly used variables such as user_info which are passed as context to django's render function
# and creates the react root variable.
# the django render function calls an html template that extends the base and does two things:
# 1
#   calls any static JSX component needed for the page rendering
# 2
#   structures the react render (a method of the root variable)
#   with all the components that were loaded


def home(request: HttpRequest):
    return render(request, 'main/home.html')


@login_required
def create_checklist(request: HttpRequest):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    if request.method == 'POST':
        return HttpResponse('CHOCHO')
    
    form = ChecklistCreateForm()
    questions = ChecklistQuestion.objects.filter(template=True).all()

    # HEY. maybe this is a way to acces individual fields from forms in the template
    form.fields['template'].initial = True

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
        return HttpResponse('CHOCHO')
    
    form = ChecklistQuestionCreateForm()

    # HEY. maybe this is a way to acces individual fields from forms in the template
    form.fields['template'].initial = True

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
