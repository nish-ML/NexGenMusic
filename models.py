from django.db import models
from django.contrib.auth.models import User

# -------------------------------
# Mood Detection model
# -------------------------------
class MoodDetection(models.Model):
    mood = models.CharField(max_length=50)

    def __str__(self):
        return self.mood


# -------------------------------
# Sentiment Analysis model
# -------------------------------
class SentimentAnalysis(models.Model):
    sentiment = models.CharField(max_length=50)

    def __str__(self):
        return self.sentiment


# -------------------------------
# Music Generation model
# -------------------------------
class MusicGeneration(models.Model):
    track_name = models.CharField(max_length=100, default='New Track')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.track_name


# -------------------------------
# Uploaded Image model
# -------------------------------
class UploadedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/')
    mood = models.CharField(max_length=100, blank=True, null=True)
    sentiment = models.CharField(max_length=100, blank=True, null=True)
    music_file = models.FileField(upload_to='music/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.mood if self.mood else 'No Mood'}"


# -------------------------------
# Search History model
# -------------------------------
class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.CharField(max_length=50, blank=True, null=True)
    sentiment = models.CharField(max_length=50, blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    song_type = models.CharField(max_length=50, blank=True, null=True)
    search_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        short_text = self.search_text[:30] + ('...' if len(self.search_text) > 30 else '')
        return f"{self.user.username} - {short_text}"
