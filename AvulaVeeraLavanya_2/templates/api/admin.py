from django.contrib import admin

from .models import GenerationHistory


@admin.register(GenerationHistory)
class GenerationHistoryAdmin(admin.ModelAdmin):
	list_display = ("id", "user", "mood", "sentiment", "duration_sec", "created_at")
	search_fields = ("prompt", "user__username", "mood", "sentiment")
	list_filter = ("mood", "sentiment", "created_at")


