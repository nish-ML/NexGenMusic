from django.db import models
from django.contrib.auth.models import User


# 🎵 Music generation records linked to each user
class MusicRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="music_records", null=True, blank=True)
    user_input = models.TextField()
    mood = models.CharField(max_length=50)
    confidence = models.FloatField()
    sentiment = models.CharField(max_length=50)
    audio_file = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.mood} ({self.sentiment})"


# 👤 Extended profile for extra user details
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
