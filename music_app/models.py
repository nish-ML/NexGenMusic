from django.db import models
from django.contrib.auth.models import User

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    prompt = models.TextField(blank=True, null=True)
    sentiment = models.CharField(max_length=100, blank=True, null=True)
    mood = models.CharField(max_length=100, blank=True, null=True)
    music_file = models.FileField(upload_to='music/', blank=True, null=True)
    # Spotify fields
    spotify_track_id = models.CharField(max_length=100, blank=True, null=True)
    spotify_track_name = models.CharField(max_length=255, blank=True, null=True)
    spotify_artists = models.TextField(blank=True, null=True)  # JSON string of artists
    spotify_external_url = models.URLField(blank=True, null=True)
    spotify_image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.prompt:
            return f"History: {self.prompt[:50]}... ({self.created_at})"
        elif self.spotify_track_name:
            return f"Spotify: {self.spotify_track_name} ({self.created_at})"
        return f"History: ({self.created_at})"
