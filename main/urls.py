from django.urls import path

from . import views, views_company, views_question, views_vehicle, views_answer, views_answer_session, views_question_type

urlpatterns = [
    path('', views.home, name='main-home'),

    path('company/add/', views_company.create_company, name='main-company_add'),
    path('company/<int:model_id>/', views_company.update_company, name='main-company_update'),
    path('company/<int:model_id>/delete/', views_company.delete_company, name='main-company_delete'),

    path('vehicle/add/', views_vehicle.create_vehicle, name='main-vehicle_add'),
    path('vehicle/<int:model_id>/', views_vehicle.update_vehicle, name='main-vehicle_update'),
    path('vehicle/<int:model_id>/delete/', views_vehicle.delete_vehicle, name='main-vehicle_delete'),

    path('question/', views_question.questions, name='main-question'),
    path('question/add/', views_question.create_question, name='main-question_add'),
    path('question/<int:model_id>/', views_question.update_question, name='main-question_update'),
    path('question/delete/<int:model_id>/', views_question.delete_question, name='main-question_delete'),

    path('question_type/add/', views_question_type.create_question_type, name='main-question_type_add'),
    path('question_type/<int:model_id>/', views_question_type.update_question_type, name='main-question_type_update'),
    path('question_type/<int:model_id>/delete/', views_question_type.delete_question_type, name='main-question_type_delete'),

    path('answers/', views_answer.answers, name='main-answers'),
    path('answer/<int:answer_id>/', views_answer.answer, name='main-answer'),

    # path('questions_answer/', views.questions_answer, name='main-questions_answer'),
    # path('question_answer/<int:vehicle_id>/<int:question_template_id>', views.question_answer, name='main-question_answer'),
    path('answer_session_portal/<int:vehicle_id>', views_answer_session.questions_answer_portal, name='main-answer_session_potral'),
    path('answer_session/<int:vehicle_id>/<int:question_type_id>/<int:page>', views_answer_session.questions_answer_session, name='main-answer_session'),

    #path('api/<str:url_name>/<int:model_id>/', views.api_single, name='api-single'),
    #path('api/<str:url_name>/', views.api_multiple, name='api-multiple'),

    path('hello_world/', views.hello_world, name='main-hello_world'),
    path('test/', views.test, name='main-test'),
]