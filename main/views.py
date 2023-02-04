from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


def hello_world(request: HttpRequest):
    return HttpResponse('Hello, world!')
