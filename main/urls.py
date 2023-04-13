from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='main-home'),
    path('checklist/', views.checklists, name='main-checklist'),
    path('checklist/add/', views.create_checklist, name='main-checklist_add'),
    path('checklist/<int:checklist_id>/', views.update_checklist, name='main-checklist_update'),
    path('checklist/<int:checklist_id>/delete/', views.delete_checklist, name='main-checklist_delete'),

    path('question/', views.questions, name='main-question'),
    path('question/add/', views.create_question, name='main-question_add'),
    path('question/<int:question_id>/', views.update_question, name='main-question_update'),
    path('question/delete/<int:question_id>/', views.delete_question, name='main-question_delete'),

    #path('api/<str:url_name>/<int:model_id>/', views.api_single, name='api-single'),
    #path('api/<str:url_name>/', views.api_multiple, name='api-multiple'),

    path('hello_world/', views.hello_world, name='main-hello_world'),
    path('test/', views.test, name='main-test'),
]