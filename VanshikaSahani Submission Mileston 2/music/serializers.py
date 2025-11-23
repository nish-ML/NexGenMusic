from rest_framework import serializers
from .models import MusicRecord

class MusicRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicRecord
        fields = '__all__'
