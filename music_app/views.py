
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout
from .utils.bert_sentiment import predict_sentiment
from .utils.mood_predictor import predict_mood
from .utils.musicgen_model import generate_music
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
            data.append({
                "id": h.id,
                "prompt": h.prompt,
                "sentiment": h.sentiment,
                "mood": h.mood,
                "music_url": music_url,
                "created_at": h.created_at.isoformat()
            })
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

def home(request):
    context = {}

    if request.method == "POST":
        prompt = request.POST.get("text")
        duration = int(request.POST.get("duration", 30))  # Get duration from form
        duration = max(5, min(30, duration))  # Clamp between 5-30 seconds

        # Step 1: Sentiment Analysis
        sentiment = predict_sentiment(prompt)

        # Step 2: Mood Detection
        mood = predict_mood(prompt)

        # Step 3: Generate Music with custom duration
        music_path = generate_music(f"{mood} instrumental based on {sentiment} mood", duration)

        music_url = None
        if music_path:
            # Convert filesystem path to media URL
            music_filename = os.path.basename(music_path)
            music_url = settings.MEDIA_URL + music_filename

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
        }

    return render(request, "home.html", context)
