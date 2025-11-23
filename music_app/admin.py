from django.contrib import admin
from .models import History

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'prompt', 'sentiment', 'mood', 'created_at')
    list_filter = ('user', 'sentiment', 'mood', 'created_at')
    search_fields = ('prompt', 'user__username')
