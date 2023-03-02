from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    url_name = 'profile'
    class Meta:
        model = Profile
        depth = 1
        read_only_fields = '__all__'