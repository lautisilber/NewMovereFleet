from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='main-home'),
    path('hello_world/', views.hello_world, name='main-hello_world'),
    path('test/', views.test, name='main-test'),
]