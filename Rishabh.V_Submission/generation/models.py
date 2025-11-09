from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return self.user.username

class MusicTrack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="music_tracks")
    title = models.CharField(max_length=255)
    prompt = models.TextField()
    mood = models.CharField(max_length=50)
    sentiment = models.CharField(max_length=50)
    generated_music = models.FileField(upload_to='music_tracks/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"