from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

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
    context = {
        'user_info': True,
        'home_link': True
    }
    return render(request, 'main/home.html', context=context)


### utils views

def hello_world(request: HttpRequest):
    return HttpResponse('Hello, world!')


def test(request:HttpRequest):
    context = {
        'user_info': True
    }
    return render(request, 'main/test.html', context=context)
