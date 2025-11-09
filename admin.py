from django.contrib import admin
from .models import MoodDetection, SentimentAnalysis, MusicGeneration, UploadedImage, SearchHistory


# Register all models in the Django admin panel
@admin.register(MoodDetection)
class MoodDetectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'mood')
    search_fields = ('mood',)


@admin.register(SentimentAnalysis)
class SentimentAnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'sentiment')
    search_fields = ('sentiment',)


@admin.register(MusicGeneration)
class MusicGenerationAdmin(admin.ModelAdmin):
    list_display = ('id', 'track_name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('track_name',)


@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'mood', 'sentiment', 'uploaded_at')
    list_filter = ('uploaded_at', 'mood')
    search_fields = ('user__username', 'mood')


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'mood', 'search_text', 'created_at')
    list_filter = ('created_at', 'mood')
    search_fields = ('user__username', 'search_text')
