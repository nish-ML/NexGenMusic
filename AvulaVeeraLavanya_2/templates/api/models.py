from django.conf import settings
from django.db import models


class GenerationHistory(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="generations")
	prompt = models.TextField()
	mood = models.CharField(max_length=64)
	sentiment = models.CharField(max_length=32)
	audio_file = models.FileField(upload_to="generated/")
	duration_sec = models.PositiveIntegerField(default=10)
	model_name = models.CharField(max_length=128, default="facebook/musicgen-small")
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]


