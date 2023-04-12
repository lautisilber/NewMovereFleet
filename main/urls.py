from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='main-home'),
    path('checklist/add/', views.create_checklist, name='main-checklist_add'),
    path('question/', views.questions, name='main-question'),
    path('question/add/', views.create_question, name='main-question_add'),
    path('question/<int:question_id>/', views.update_question, name='main-question_update'),
    path('hello_world/', views.hello_world, name='main-hello_world'),
    path('test/', views.test, name='main-test'),
]