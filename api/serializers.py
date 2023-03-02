from rest_framework import serializers
from .models import ApiTest


class ApiTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiTest
        fields = '__all__'