from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .utils.bert_sentiment import predict_sentiment
from .utils.mood_predictor import predict_mood
from .utils.musicgen_model import generate_music
from .utils.spotify_api import search_tracks, get_recommendations, get_genres
from django.conf import settings
from .models import History
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import os

def history_api(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            histories = History.objects.filter(user=request.user).order_by('-created_at')
        else:
            histories = History.objects.none()
        data = []
        for h in histories:
            music_url = h.music_file.url if h.music_file else None
            item = {
                "id": h.id,
                "created_at": h.created_at.isoformat()
            }
            if h.prompt:
                item.update({
                    "type": "generated",
                    "prompt": h.prompt,
                    "sentiment": h.sentiment,
                    "mood": h.mood,
                    "music_url": music_url
                })
            elif h.spotify_track_name:
                item.update({
                    "type": "spotify",
                    "spotify_track_name": h.spotify_track_name,
                    "spotify_artists": h.spotify_artists.split(',') if h.spotify_artists else [],
                    "spotify_external_url": h.spotify_external_url,
                    "spotify_image_url": h.spotify_image_url
                })
            data.append(item)
        return JsonResponse({"history": data}, safe=False)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@api_view(['POST'])
def register_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)
    refresh = RefreshToken.for_user(user)
    return Response({
        'message': 'User created successfully',
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response({
        'message': 'Login successful',
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }, status=status.HTTP_200_OK)

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)
        return redirect('home')

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_profile':
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')

            # Check if username is taken by another user
            if User.objects.filter(username=username).exclude(id=request.user.id).exists():
                messages.error(request, 'Username already exists')
                return redirect('profile')

            request.user.username = username
            request.user.email = email
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.save()

            messages.success(request, 'Profile updated successfully')
            return redirect('profile')

        elif action == 'change_password':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully')
                return redirect('profile')
            else:
                for error in form.errors.values():
                    messages.error(request, error[0])
                return redirect('profile')

        elif action == 'delete_account':
            # Delete all user's history first
            History.objects.filter(user=request.user).delete()
            # Delete the user
            request.user.delete()
            logout(request)
            messages.success(request, 'Account deleted successfully')
            return redirect('home')

    # Get user stats
    user_history_count = History.objects.filter(user=request.user, prompt__isnull=False).count()
    spotify_saves_count = History.objects.filter(user=request.user, spotify_track_name__isnull=False).count()

    # Get recent activity (last 10 items)
    recent_activity = History.objects.filter(user=request.user).order_by('-created_at')[:10]

    context = {
        'user_history_count': user_history_count,
        'spotify_saves_count': spotify_saves_count,
        'recent_activity': recent_activity,
    }

    return render(request, 'profile.html', context)

@login_required
def history_view(request):
    # Get filter parameters
    type_filter = request.GET.get('type', '')
    mood_filter = request.GET.get('mood', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    # Base queryset
    history_items = History.objects.filter(user=request.user).order_by('-created_at')

    # Apply filters
    if type_filter:
        if type_filter == 'generated':
            history_items = history_items.filter(prompt__isnull=False)
        elif type_filter == 'spotify':
            history_items = history_items.filter(spotify_track_name__isnull=False)

    if mood_filter:
        history_items = history_items.filter(mood__iexact=mood_filter)

    if date_from:
        history_items = history_items.filter(created_at__date__gte=date_from)

    if date_to:
        history_items = history_items.filter(created_at__date__lte=date_to)

    # Add type and duration fields for template
    for item in history_items:
        if item.prompt:
            item.type = 'generated'
            # Extract duration from music file name if available
            if item.music_file:
                filename = item.music_file.name
                if '_5s.' in filename:
                    item.duration = 5
                elif '_10s.' in filename:
                    item.duration = 10
                elif '_15s.' in filename:
                    item.duration = 15
                elif '_20s.' in filename:
                    item.duration = 20
                elif '_30s.' in filename:
                    item.duration = 30
        elif item.spotify_track_name:
            item.type = 'spotify'

    # Pagination
    paginator = Paginator(history_items, 12)  # 12 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'history_items': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'paginator': paginator,
    }

    return render(request, 'history.html', context)

@api_view(['POST'])
def theme_api(request):
    """API endpoint to save user's theme preference"""
    theme = request.data.get('theme', 'light')
    request.session['theme'] = theme
    return Response({'message': 'Theme updated successfully'})

def home(request):
    context = {}

    if request.method == "POST":
        action = request.POST.get("action")
        prompt = request.POST.get("text")
        duration = int(request.POST.get("duration", 30))  # Get duration from form
        duration = max(5, min(30, duration))  # Clamp between 5-30 seconds

        if action == "generate":
            # Step 1: Sentiment Analysis
            sentiment = predict_sentiment(prompt)

            # Step 2: Mood Detection
            mood = predict_mood(prompt)

            # Step 3: Generate Music with custom duration
            try:
                music_path = generate_music(f"{mood} instrumental based on {sentiment} mood", duration)
                print(f"DEBUG: Music generation result: {music_path}")
            except Exception as e:
                print(f"DEBUG: Music generation error: {e}")
                music_path = None

            music_url = None
            if music_path:
                # Convert filesystem path to media URL
                music_filename = os.path.basename(music_path)
                music_url = settings.MEDIA_URL + music_filename
                print(f"DEBUG: Music URL: {music_url}")

            # Step 4: Save to History
            if music_path and request.user.is_authenticated:
                History.objects.create(
                    user=request.user,
                    prompt=prompt,
                    sentiment=sentiment,
                    mood=mood,
                    music_file=music_filename  # Save relative path
                )

            # Step 5: Pass data to template
            context = {
                "prompt": prompt,
                "sentiment": sentiment,
                "mood": mood,
                "music_url": music_url,  # ✅ This must be a URL, not a full path
                "show_spotify": True,  # Flag to show Spotify section
            }
        elif action == "spotify":
            # Step 1: Sentiment Analysis
            sentiment = predict_sentiment(prompt)

            # Step 2: Mood Detection
            mood = predict_mood(prompt)

            # Step 3: Pass data to template for Spotify discovery
            context = {
                "prompt": prompt,
                "sentiment": sentiment,
                "mood": mood,
                "show_spotify": True,  # Flag to show Spotify section
            }

    return render(request, "home.html", context)

@api_view(['GET'])
def spotify_search_api(request):
    query = request.GET.get('q')
    language = request.GET.get('language')
    limit = int(request.GET.get('limit', 10))
    if not query:
        return Response({'error': 'Query parameter "q" is required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        # Modify query based on language selection
        if language and language != 'english':
            # For Indian languages, search in Indian market and add language to query
            if language in ['hindi', 'tamil', 'telugu', 'bengali', 'marathi', 'gujarati', 'kannada', 'malayalam', 'punjabi', 'odia', 'assamese', 'maithili', 'santali']:
                query = f"{query} {language}"
                market = 'IN'
            else:
                market = None
        else:
            market = None
        tracks = search_tracks(query, limit, market=market)
        return Response({'tracks': tracks}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def spotify_recommendations_api(request):
    mood = request.GET.get('mood')
    genre = request.GET.get('genre')
    language = request.GET.get('language')
    limit = int(request.GET.get('limit', 10))
    try:
        # Map mood to Spotify genres or use provided genre
        seed_genres = [genre] if genre else None
        if mood:
            # Enhanced mapping of moods to genres for better recommendations
            mood_genre_map = {
                'happy': 'pop',
                'sad': 'indie',
                'energetic': 'rock',
                'calm': 'ambient',
                'romantic': 'r-n-b',
                'angry': 'metal',
                'excited': 'electronic'
            }
            seed_genres = [mood_genre_map.get(mood.lower(), 'pop')]

        # For Indian languages, use search instead of recommendations
        if language and language != 'english':
            if language in ['hindi', 'tamil', 'telugu', 'bengali', 'marathi', 'gujarati', 'kannada', 'malayalam', 'punjabi', 'odia', 'assamese', 'maithili', 'santali']:
                # Use search API for Indian languages - map moods to better search terms with specific language keywords
                mood_search_map = {
                    'happy': 'upbeat cheerful joyful',
                    'sad': 'melancholic emotional heartbreak',
                    'energetic': 'high energy dance party',
                    'calm': 'relaxing peaceful ambient',
                    'romantic': 'romantic love ballad',
                    'excited': 'excited celebration fun'
                }
                search_mood = mood_search_map.get(mood.lower(), mood)

                # Language-specific search terms for better results
                language_search_terms = {
                    'hindi': 'hindi bollywood hindi pop hindi indie',
                    'tamil': 'tamil tamil pop kollywood',
                    'telugu': 'telugu tollywood telugu pop',
                    'bengali': 'bengali bengali pop rabindra sangeet',
                    'marathi': 'marathi marathi pop marathi songs',
                    'gujarati': 'gujarati gujarati pop gujarati garba',
                    'kannada': 'kannada kannada pop sandalwood',
                    'malayalam': 'malayalam malayalam pop mollywood',
                    'punjabi': 'punjabi punjabi pop bhangra',
                    'odia': 'odia odia pop odia songs',
                    'assamese': 'assamese assamese pop assamese songs',
                    'maithili': 'maithili maithili songs bhojpuri',
                    'santali': 'santali santali folk santali songs'
                }

                language_terms = language_search_terms.get(language, f"{language} songs")
                query = f"{search_mood} {language_terms}"
                tracks = search_tracks(query, limit, market='IN')
                return Response({'recommendations': tracks}, status=status.HTTP_200_OK)
            else:
                market = None
        else:
            market = None

        recommendations = get_recommendations(seed_genres=seed_genres, limit=limit, market=market)
        return Response({'recommendations': recommendations}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def spotify_genres_api(request):
    try:
        genres = get_genres()
        return Response({'genres': genres}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def save_spotify_track_api(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

    track_data = request.data
    required_fields = ['id', 'name', 'artists', 'external_url']
    if not all(field in track_data for field in required_fields):
        return Response({'error': 'Missing required track data'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Check if track already saved
        existing = History.objects.filter(
            user=request.user,
            spotify_track_id=track_data['id']
        ).first()
        if existing:
            return Response({'message': 'Track already saved to history'}, status=status.HTTP_200_OK)

        # Save to history
        History.objects.create(
            user=request.user,
            spotify_track_id=track_data['id'],
            spotify_track_name=track_data['name'],
            spotify_artists=','.join(track_data['artists']),
            spotify_external_url=track_data['external_url'],
            spotify_image_url=track_data.get('image_url')
        )
        return Response({'message': 'Track saved to history successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
