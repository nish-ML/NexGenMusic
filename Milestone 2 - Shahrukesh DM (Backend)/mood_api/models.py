from django.db import models
from django.contrib.auth.models import User

class GeneratedMusic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    prompt = models.TextField()
    mood = models.CharField(max_length=50)
    confidence = models.FloatField(default=0.0)
    audio_file = models.FileField(upload_to="generated_music/")
    model_version = models.CharField(max_length=100, default="EnhancedMoodClassifier_v1")
    ai_metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'} - {self.mood} ({self.confidence:.2f})"
