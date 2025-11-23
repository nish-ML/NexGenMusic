from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    favorite_genre = models.CharField(max_length=80, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class MusicHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.CharField(max_length=80)
    genre = models.CharField(max_length=80)
    language = models.CharField(max_length=20, blank=True, null=True)
    spotify_song_url = models.URLField()
    song_name = models.CharField(max_length=255, blank=True, null=True)
    artist_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.song_name or self.spotify_song_url}"

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"

class PlaylistTrack(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='tracks')
    song_name = models.CharField(max_length=255)
    artist_name = models.CharField(max_length=255)
    spotify_url = models.URLField()
    mood = models.CharField(max_length=80, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.playlist.name} - {self.song_name}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song_name = models.CharField(max_length=255)
    artist_name = models.CharField(max_length=255)
    spotify_url = models.URLField()
    mood = models.CharField(max_length=80, blank=True, null=True)
    genre = models.CharField(max_length=80, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'spotify_url')

    def __str__(self):
        return f"{self.user.username} - {self.song_name}"

class Download(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song_name = models.CharField(max_length=255)
    artist_name = models.CharField(max_length=255)
    file_url = models.URLField()
    file_type = models.CharField(max_length=20)  # 'audio', 'midi', 'wav'
    mood = models.CharField(max_length=80, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.song_name}"
