from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='main-home'),

    path('company/', views.companies, name='main-company'),
    path('company/add/', views.create_company, name='main-company_add'),
    path('company/<int:model_id>/', views.update_company, name='main-company_update'),
    path('company/<int:model_id>/delete/', views.delete_company, name='main-company_delete'),

    path('vehicle/', views.vehicles, name='main-vehicle'),
    path('vehicle/add/', views.create_vehicle, name='main-vehicle_add'),
    path('vehicle/<int:model_id>/', views.update_vehicle, name='main-vehicle_update'),
    path('vehicle/<int:model_id>/delete/', views.delete_vehicle, name='main-vehicle_delete'),

    path('question/', views.questions, name='main-question'),
    path('question/add/', views.create_question, name='main-question_add'),
    path('question/<int:model_id>/', views.update_question, name='main-question_update'),
    path('question/delete/<int:model_id>/', views.delete_question, name='main-question_delete'),

    path('questions_answer/', views.questions_answer, name='main-questions_answer'),
    path('question_answer/<int:question_template_id>', views.question_answer, name='main-question_answer'),

    #path('api/<str:url_name>/<int:model_id>/', views.api_single, name='api-single'),
    #path('api/<str:url_name>/', views.api_multiple, name='api-multiple'),

    path('hello_world/', views.hello_world, name='main-hello_world'),
    path('test/', views.test, name='main-test'),
]