from django.db import models
from django.contrib.auth.models import User

class GenerationHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generations')
    input_text = models.TextField()
    mood = models.CharField(max_length=32)
    sentiment = models.CharField(max_length=32)
    audio_file = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.mood}'
