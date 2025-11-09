from rest_framework import serializers
from .models import GeneratedMusic

class GeneratedMusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedMusic
        fields = "__all__"
        fields = ['id', 'prompt', 'mood', 'audio_file', 'created_at']
