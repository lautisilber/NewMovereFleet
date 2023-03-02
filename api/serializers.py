from rest_framework import serializers
from .models import ApiTest


class ApiTestSerializer(serializers.ModelSerializer):
    url_name = 'api_test'
    class Meta:
        model = ApiTest
        fields = '__all__'