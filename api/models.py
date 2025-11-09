from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class MusicHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    spotify_song_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
