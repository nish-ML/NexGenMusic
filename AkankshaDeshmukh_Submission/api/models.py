from django.db import models
from django.contrib.auth.models import User

class GeneratedMusic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    prompt = models.TextField()
    mood = models.CharField(max_length=50)
    audio_file = models.FileField(upload_to="generated_music/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.mood}"
