import json
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import MusicHistory, UserProfile, Playlist, PlaylistTrack, Favorite, Download
from .serializers import (MusicHistorySerializer, UserProfileSerializer, PlaylistSerializer, 
                         PlaylistTrackSerializer, FavoriteSerializer, DownloadSerializer)
from .spotify_client import get_song_by_mood_genre_language, get_playlist_by_mood_genre_language, get_recommendations_by_mood
from .ml_mood_predictor import predict_mood_and_sentiment, analyze_text_sentiment
from .music_generator import get_music_generator
# Import audio generator with error handling
try:
    from .audio_generator import get_audio_generator
    AUDIO_GENERATOR_AVAILABLE = True
except Exception as e:
    print(f"Warning: Audio generator import failed: {e}")
    AUDIO_GENERATOR_AVAILABLE = False
    get_audio_generator = None

try:
    from .midi_music_generator import get_midi_generator
    MIDI_GENERATOR_AVAILABLE = True
except ImportError as e:
    print(f"Warning: MIDI generator not available: {e}")
    MIDI_GENERATOR_AVAILABLE = False
    get_midi_generator = None
import os
from django.http import FileResponse, Http404

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_audio(request):
    """
    Generate 40-second audio clip based on mood and sentiment
    Accepts JSON: { "title": optional string, "mood": optional string, "text": optional text for mood pred, "intensity": optional float }
    """
    user = request.user
    title = (request.data.get('title') or "").strip() or None
    mood = (request.data.get('mood') or "").strip() or None
    text = (request.data.get('text') or "").strip() or None
    intensity = request.data.get('intensity', 0.5)
    
    # Validate intensity
    try:
        intensity = float(intensity)
        intensity = max(0.0, min(intensity, 1.0))
    except:
        intensity = 0.5
    
    # Predict mood from text if not provided
    sentiment_analysis = None
    sentiment_score = 0.0
    
    if not mood and text:
        predicted_mood, polarity, confidence, emotions = predict_mood_and_sentiment(text)
        mood = predicted_mood
        sentiment_score = polarity
        intensity = confidence
        sentiment_analysis = {
            'mood': predicted_mood,
            'sentiment_score': polarity,
            'confidence': confidence,
            'emotions': emotions
        }
    elif text:
        _, polarity, confidence, emotions = predict_mood_and_sentiment(text)
        sentiment_score = polarity
        sentiment_analysis = {
            'mood': mood,
            'sentiment_score': polarity,
            'confidence': confidence,
            'emotions': emotions
        }
    
    if not mood:
        return Response({'error': 'Mood not provided and no text to predict from'}, status=400)
    
    try:
        if not AUDIO_GENERATOR_AVAILABLE:
            return Response({
                'error': 'Audio generation not available. Please ensure you are running in the virtual environment with: pip install soundfile scipy'
            }, status=500)
        
        # Generate audio
        audio_generator = get_audio_generator()
        audio_filepath = audio_generator.generate_mood_audio(mood, sentiment_score, intensity)
        
        # Save generation info in history
        song_title = title if title else f"{mood.title()} Audio Clip"
        MusicHistory.objects.create(
            user=user,
            mood=mood,
            genre="Generated Audio",
            language="",
            spotify_song_url=f"/api/audio/{os.path.basename(audio_filepath)}",
            song_name=song_title,
            artist_name="NexGenMusic AI"
        )
        
        response_data = {
            'audio_url': f"/api/audio/{os.path.basename(audio_filepath)}",
            'mood': mood,
            'intensity': intensity,
            'sentiment_score': sentiment_score,
            'duration': 40,
            'filename': os.path.basename(audio_filepath)
        }
        
        if sentiment_analysis:
            response_data['sentiment_analysis'] = sentiment_analysis
        
        return Response(response_data)
        
    except Exception as e:
        return Response({'error': f'Failed to generate audio: {str(e)}'}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_midi_music(request):
    """
    Generate MIDI-based music from mood detection
    Accepts JSON: { "text": string, "duration": optional int (default 40) }
    """
    user = request.user
    text = (request.data.get('text') or "").strip()
    duration = request.data.get('duration', 40)
    
    if not text:
        return Response({'error': 'Text is required for music generation'}, status=400)
    
    # Validate duration
    try:
        duration = int(duration)
        duration = max(10, min(duration, 120))  # Between 10 and 120 seconds
    except:
        duration = 40
    
    try:
        if not MIDI_GENERATOR_AVAILABLE:
            return Response({'error': 'MIDI generation not available. Please install required libraries: pip install midiutil'}, status=500)
        
        # Generate MIDI music
        midi_generator = get_midi_generator()
        result = midi_generator.generate_music_from_text(text, duration)
        
        # Save generation info in history
        MusicHistory.objects.create(
            user=user,
            mood=result['mood'],
            genre="MIDI Generated",
            language="",
            spotify_song_url=f"/api/music/{os.path.basename(result['midi_file'])}",
            song_name=f"{result['mood'].title()} MIDI Melody",
            artist_name="NexGenMusic MIDI AI"
        )
        
        response_data = {
            'midi_url': f"/api/music/{os.path.basename(result['midi_file'])}",
            'wav_url': f"/api/music/{os.path.basename(result['wav_file'])}" if result['wav_file'] else None,
            'mood': result['mood'],
            'tempo': result['tempo'],
            'duration': result['duration'],
            'sentiment_score': result['sentiment_score'],
            'confidence': result['confidence'],
            'melody_length': result['melody_length'],
            'instrument': result['instrument'],
            'notes_used': result['notes_used']
        }
        
        return Response(response_data)
        
    except Exception as e:
        return Response({'error': f'Failed to generate MIDI music: {str(e)}'}, status=500)

@api_view(['GET'])
def serve_audio(request, filename):
    """
    Serve generated audio files
    """
    audio_dir = "generated_audio"
    filepath = os.path.join(audio_dir, filename)
    
    if not os.path.exists(filepath):
        raise Http404("Audio file not found")
    
    return FileResponse(
        open(filepath, 'rb'),
        as_attachment=False,
        content_type='audio/wav'
    )

@api_view(['GET'])
def serve_music(request, filename):
    """
    Serve generated MIDI/music files
    """
    music_dir = "generated_music"
    filepath = os.path.join(music_dir, filename)
    
    if not os.path.exists(filepath):
        raise Http404("Music file not found")
    
    content_type = 'audio/midi' if filename.endswith('.mid') else 'audio/wav'
    
    return FileResponse(
        open(filepath, 'rb'),
        as_attachment=False,
        content_type=content_type
    )

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'username and password required'}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({'error': 'username already exists'}, status=400)
    user = User.objects.create_user(username=username, password=password)
    refresh = RefreshToken.for_user(user)
    return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
    return Response({'error': 'Invalid credentials'}, status=401)

@api_view(['GET'])
@permission_classes([])
def google_auth(request):
    """Redirect to Google authorization"""
    from .google_auth import get_google_auth_url
    from django.shortcuts import redirect
    auth_url = get_google_auth_url()
    return redirect(auth_url)

@api_view(['GET'])
@permission_classes([])
def google_callback(request):
    """Handle Google OAuth callback"""
    from .google_auth import get_google_token, get_google_user_info
    from django.shortcuts import redirect
    
    code = request.GET.get('code')
    error = request.GET.get('error')
    
    if error:
        return redirect(f'/neon-login.html?error=google_auth_failed')
    
    if not code:
        return redirect(f'/neon-login.html?error=no_code')
    
    try:
        # Get access token
        token_data = get_google_token(code)
        access_token = token_data.get('access_token')
        
        if not access_token:
            return redirect(f'/neon-login.html?error=token_failed')
        
        # Get user info
        user_info = get_google_user_info(access_token)
        google_id = user_info.get('id')
        email = user_info.get('email')
        name = user_info.get('name', email)
        
        # Create or get user
        username = f"google_{google_id}"
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'first_name': name}
        )
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        refresh_token = str(refresh)
        
        # Redirect to dashboard with tokens
        return redirect(f'/dashboard/?access={access}&refresh={refresh_token}&google=true')
        
    except Exception as e:
        print(f"Google auth error: {e}")
        return redirect(f'/neon-login.html?error=auth_exception')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_music(request):
    """
    Accepts JSON:
    { "mood": optional string, "genre": optional string, "text": optional text for mood pred, "language": optional string (e.g. 'english' or 'hindi' or 'en' ) }
    """
    user = request.user
    mood = (request.data.get('mood') or "").strip() or None
    genre = (request.data.get('genre') or "").strip() or None
    text = (request.data.get('text') or "").strip() or None
    language = (request.data.get('language') or "").strip() or None

    # Predict mood from text when mood not provided
    sentiment_analysis = None
    if not mood and text:
        predicted_mood, polarity, confidence, emotions = predict_mood_and_sentiment(text)
        mood = predicted_mood
        sentiment_analysis = {
            'mood': predicted_mood,
            'sentiment_score': polarity,
            'confidence': confidence,
            'emotions': emotions
        }
    elif text:
        _, polarity, confidence, emotions = predict_mood_and_sentiment(text)
        sentiment_analysis = {
            'mood': mood,
            'sentiment_score': polarity,
            'confidence': confidence,
            'emotions': emotions
        }

    if not mood:
        return Response({'error': 'Mood not provided and no text to predict from'}, status=400)

    # Search Spotify
    spotify_url, song_name, artist_name = get_song_by_mood_genre_language(mood, genre or "", language)

    if not spotify_url:
        return Response({'error': 'No song found for that mood/genre/language'}, status=404)

    # Save in history
    history = MusicHistory.objects.create(
        user=user, mood=mood, genre=(genre or ""), language=(language or ""), spotify_song_url=spotify_url,
        song_name=song_name, artist_name=artist_name
    )

    response_data = {
        'spotify_url': spotify_url,
        'song_name': song_name,
        'artist_name': artist_name,
        'mood': mood,
        'genre': genre
    }
    
    if sentiment_analysis:
        response_data['sentiment_analysis'] = sentiment_analysis

    return Response(response_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history(request):
    user = request.user
    qs = MusicHistory.objects.filter(user=user).order_by('-created_at')[:50]
    serializer = MusicHistorySerializer(qs, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_playlist(request):
    """
    Generate a playlist using ML-based mood prediction and intelligent music selection
    Accepts JSON:
    { "mood": optional string, "genre": optional string, "text": optional text for mood pred, "language": optional string, "limit": optional int (default 10) }
    """
    user = request.user
    mood = (request.data.get('mood') or "").strip() or None
    genre = (request.data.get('genre') or "").strip() or None
    text = (request.data.get('text') or "").strip() or None
    language = (request.data.get('language') or "").strip() or None
    limit = request.data.get('limit', 10)
    
    # Validate limit
    try:
        limit = int(limit)
        limit = max(5, min(limit, 50))  # Between 5 and 50
    except:
        limit = 10

    # Predict mood from text using ML model
    sentiment_analysis = None
    intensity = 0.5
    
    if not mood and text:
        predicted_mood, polarity, confidence, emotions = predict_mood_and_sentiment(text)
        mood = predicted_mood
        intensity = confidence
        sentiment_analysis = {
            'mood': predicted_mood,
            'sentiment_score': polarity,
            'confidence': confidence,
            'emotions': emotions,
            'model_used': emotions.get('method', 'transformer')
        }
    elif text:
        _, polarity, confidence, emotions = predict_mood_and_sentiment(text)
        intensity = confidence
        sentiment_analysis = {
            'mood': mood,
            'sentiment_score': polarity,
            'confidence': confidence,
            'emotions': emotions,
            'model_used': emotions.get('method', 'transformer')
        }

    if not mood:
        return Response({'error': 'Mood not provided and no text to predict from'}, status=400)

    # Use ML-based music generator
    try:
        music_generator = get_music_generator()
        playlist = music_generator.generate_playlist(
            mood=mood,
            genre=genre,
            language=language,
            intensity=intensity,
            limit=limit
        )
    except Exception as e:
        print(f"Music generator error: {e}")
        # Fallback to basic search
        try:
            playlist = get_playlist_by_mood_genre_language(mood, genre or "", language, limit)
        except:
            return Response({'error': 'Failed to generate playlist'}, status=500)

    if not playlist:
        return Response({'error': 'No songs found for that mood/genre/language'}, status=404)

    # Save first track in history for tracking
    if playlist:
        first_track = playlist[0]
        MusicHistory.objects.create(
            user=user, 
            mood=mood, 
            genre=(genre or ""), 
            language=(language or ""), 
            spotify_song_url=first_track['spotify_url'],
            song_name=first_track['song_name'], 
            artist_name=first_track['artist_name']
        )

    response_data = {
        'playlist': playlist,
        'mood': mood,
        'genre': genre,
        'playlist_size': len(playlist),
        'intensity': intensity
    }
    
    if sentiment_analysis:
        response_data['sentiment_analysis'] = sentiment_analysis

    return Response(response_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyze_sentiment(request):
    """
    Analyze sentiment from text
    Accepts JSON: { "text": string }
    """
    text = (request.data.get('text') or "").strip()
    
    if not text:
        return Response({'error': 'Text is required for sentiment analysis'}, status=400)
    
    analysis = analyze_text_sentiment(text)
    
    return Response(analysis)


# User Profile Views
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'GET':
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        profile.bio = request.data.get('bio', profile.bio)
        profile.favorite_genre = request.data.get('favorite_genre', profile.favorite_genre)
        profile.save()
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

# Playlist Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def playlists(request):
    if request.method == 'GET':
        playlists = Playlist.objects.filter(user=request.user).order_by('-created_at')
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        name = request.data.get('name')
        description = request.data.get('description', '')
        if not name:
            return Response({'error': 'Name is required'}, status=400)
        
        playlist = Playlist.objects.create(
            user=request.user,
            name=name,
            description=description
        )
        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data, status=201)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def playlist_detail(request, pk):
    try:
        playlist = Playlist.objects.get(pk=pk, user=request.user)
    except Playlist.DoesNotExist:
        return Response({'error': 'Playlist not found'}, status=404)
    
    if request.method == 'GET':
        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        playlist.name = request.data.get('name', playlist.name)
        playlist.description = request.data.get('description', playlist.description)
        playlist.save()
        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        playlist.delete()
        return Response(status=204)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_playlist(request, pk):
    try:
        playlist = Playlist.objects.get(pk=pk, user=request.user)
    except Playlist.DoesNotExist:
        return Response({'error': 'Playlist not found'}, status=404)
    
    song_name = request.data.get('song_name')
    artist_name = request.data.get('artist_name')
    spotify_url = request.data.get('spotify_url')
    mood = request.data.get('mood', '')
    
    if not all([song_name, artist_name, spotify_url]):
        return Response({'error': 'Missing required fields'}, status=400)
    
    track = PlaylistTrack.objects.create(
        playlist=playlist,
        song_name=song_name,
        artist_name=artist_name,
        spotify_url=spotify_url,
        mood=mood
    )
    serializer = PlaylistTrackSerializer(track)
    return Response(serializer.data, status=201)

# Favorites Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def favorites(request):
    if request.method == 'GET':
        favorites = Favorite.objects.filter(user=request.user).order_by('-created_at')
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        song_name = request.data.get('song_name')
        artist_name = request.data.get('artist_name')
        spotify_url = request.data.get('spotify_url')
        mood = request.data.get('mood', '')
        genre = request.data.get('genre', '')
        
        if not all([song_name, artist_name, spotify_url]):
            return Response({'error': 'Missing required fields'}, status=400)
        
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            spotify_url=spotify_url,
            defaults={
                'song_name': song_name,
                'artist_name': artist_name,
                'mood': mood,
                'genre': genre
            }
        )
        
        if not created:
            return Response({'message': 'Already in favorites'}, status=200)
        
        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data, status=201)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def favorite_detail(request, pk):
    try:
        favorite = Favorite.objects.get(pk=pk, user=request.user)
        favorite.delete()
        return Response(status=204)
    except Favorite.DoesNotExist:
        return Response({'error': 'Favorite not found'}, status=404)

# Downloads Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def downloads(request):
    if request.method == 'GET':
        downloads = Download.objects.filter(user=request.user).order_by('-created_at')
        serializer = DownloadSerializer(downloads, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        song_name = request.data.get('song_name')
        artist_name = request.data.get('artist_name')
        file_url = request.data.get('file_url')
        file_type = request.data.get('file_type', 'audio')
        mood = request.data.get('mood', '')
        
        if not all([song_name, artist_name, file_url]):
            return Response({'error': 'Missing required fields'}, status=400)
        
        download = Download.objects.create(
            user=request.user,
            song_name=song_name,
            artist_name=artist_name,
            file_url=file_url,
            file_type=file_type,
            mood=mood
        )
        serializer = DownloadSerializer(download)
        return Response(serializer.data, status=201)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def download_detail(request, pk):
    try:
        download = Download.objects.get(pk=pk, user=request.user)
        download.delete()
        return Response(status=204)
    except Download.DoesNotExist:
        return Response({'error': 'Download not found'}, status=404)
