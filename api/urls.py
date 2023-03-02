from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('api_test/', views.api_test, name='api-apitest'),
    path('api_test/<int:id>', views.api_test_id, name='api-apitest_id'),
]

urlpatterns = format_suffix_patterns(urlpatterns)