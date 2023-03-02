from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='main-home'),
    path('checklist/create', views.create_checklist, name='main-checklist_create'),
    path('question/create', views.create_question, name='main-question_create'),
    path('hello_world/', views.hello_world, name='main-hello_world'),
    path('test/', views.test, name='main-test'),
]