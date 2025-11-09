from rest_framework import serializers
from django.contrib.auth.models import User
from .models import GenerationHistory

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GenerationHistory
        fields = ['id', 'input_text', 'mood', 'sentiment', 'audio_file', 'created_at']

class MusicRequestSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=500, min_length=1, required=True)
    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Text cannot be empty")
        return value.strip()

class MusicResponseSerializer(serializers.Serializer):
    mood = serializers.CharField()
    sentiment = serializers.CharField()
    audio_file = serializers.CharField()
    message = serializers.CharField()
