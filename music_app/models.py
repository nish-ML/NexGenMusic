from django.db import models
from django.contrib.auth.models import User

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    prompt = models.TextField()
    sentiment = models.CharField(max_length=100)
    mood = models.CharField(max_length=100)
    music_file = models.FileField(upload_to='music/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History: {self.prompt[:50]}... ({self.created_at})"
