from rest_framework import serializers
from .models import MusicHistory, UserProfile, Playlist, PlaylistTrack, Favorite, Download
from django.contrib.auth.models import User

class MusicHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicHistory
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'bio', 'avatar_url', 'favorite_genre', 'created_at']

class PlaylistTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistTrack
        fields = '__all__'

class PlaylistSerializer(serializers.ModelSerializer):
    tracks = PlaylistTrackSerializer(many=True, read_only=True)
    track_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Playlist
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'tracks', 'track_count']
    
    def get_track_count(self, obj):
        return obj.tracks.count()

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

class DownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Download
        fields = '__all__'
