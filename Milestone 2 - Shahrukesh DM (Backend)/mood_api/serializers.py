from rest_framework import serializers
from .models import GeneratedMusic

class GeneratedMusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedMusic
        fields = '__all__'
