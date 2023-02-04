from django.urls import path

from . import views

urlpatterns = [
    path('test/', views.test, name='api-test'),
    path('get/all/<str:model_name>/', views.get_all, name='api-get_all'),
    path('get/first/<str:model_name>/', views.get_first, name='api-get_first'),
    path('post/<str:model_name>/', views.post, name='api-post'),
    path('delete/<str:model_name>/<int:id>/', views.delete, name='api-delete'),
]