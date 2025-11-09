from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MusicTrack

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class MusicTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicTrack
        fields = '__all__'
