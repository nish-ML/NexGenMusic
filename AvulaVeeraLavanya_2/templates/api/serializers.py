from django.contrib.auth.models import User
from rest_framework import serializers

from .models import GenerationHistory


class RegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, min_length=8)

	class Meta:
		model = User
		fields = ("username", "email", "password")

	def create(self, validated_data):
		user = User.objects.create_user(
			username=validated_data["username"],
			email=validated_data.get("email", ""),
			password=validated_data["password"],
		)
		return user


class GenerationHistorySerializer(serializers.ModelSerializer):
	class Meta:
		model = GenerationHistory
		fields = (
			"id",
			"prompt",
			"mood",
			"sentiment",
			"audio_file",
			"duration_sec",
			"model_name",
			"created_at",
		)


