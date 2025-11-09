
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import MusicHistory
from .serializers import UserSerializer, MusicHistorySerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .spotify_client import get_song_by_mood_genre
import random

# ---- Register API ----
@api_view(['POST'])
def register(request):
    username = request.data['username']
    password = request.data['password']
    user = User.objects.create_user(username=username, password=password)
    refresh = RefreshToken.for_user(user)
    return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})

# ---- Login API ----
@api_view(['POST'])
def login(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
    return Response({'error': 'Invalid credentials'})

# ---- History API ----
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history(request):
    history = MusicHistory.objects.filter(user=request.user)
    serializer = MusicHistorySerializer(history, many=True)
    return Response(serializer.data)

# ---- Music + Mood Generation ----
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_music(request):
    user = request.user
    mood = request.data.get("mood", "").lower()
    genre = request.data.get("genre", "").lower()

    # 🧠 Simple Mood Prediction Logic (Dummy AI Simulation)
    mood_keywords = {
        "happy": ["cheerful", "joyful", "upbeat"],
        "sad": ["melancholy", "heartfelt", "slow"],
        "energetic": ["powerful", "fast", "motivational"],
        "romantic": ["soft", "love", "emotional"]
    }

    predicted_mood = "neutral"
    for key, keywords in mood_keywords.items():
        if key in mood:
            predicted_mood = key
            break

    # 🎵 Spotify mock (simulate Spotify track)
    songs = {
        "happy": {
            "song_name": "Happy Vibes",
            "artist_name": "Pharrell Williams",
            "spotify_url": "https://open.spotify.com/track/60nZcImufyMA1MKQY3dcCH"
        },
        "sad": {
            "song_name": "Someone Like You",
            "artist_name": "Adele",
            "spotify_url": "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB"
        },
        "energetic": {
            "song_name": "Stronger",
            "artist_name": "Kanye West",
            "spotify_url": "https://open.spotify.com/track/4q4l1Fq9L9yXK1x5mU9Rz8"
        },
        "romantic": {
            "song_name": "Perfect",
            "artist_name": "Ed Sheeran",
            "spotify_url": "https://open.spotify.com/track/0tgVpDi06FyKpA1z0VMD4v"
        },
        "neutral": {
            "song_name": "Random Chill",
            "artist_name": "Lo-Fi Beats",
            "spotify_url": "https://open.spotify.com/track/1"
        }
    }

    selected = songs.get(predicted_mood, songs["neutral"])

    # 🗂️ Save in DB
    MusicHistory.objects.create(
        user=user,
        mood=predicted_mood,
        genre=genre,
        spotify_song_url=selected["spotify_url"]
    )

    return Response({
        "predicted_mood": predicted_mood,
        "song_name": selected["song_name"],
        "artist_name": selected["artist_name"],
        "spotify_url": selected["spotify_url"]
    })