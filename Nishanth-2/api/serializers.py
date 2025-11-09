from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MusicHistory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class MusicHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicHistory
        fields = '__all__'
