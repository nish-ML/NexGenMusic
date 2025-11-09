from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import timezone
from textblob import TextBlob
import os
import random
import uuid
import torch
import soundfile as sf
from transformers import MusicgenForConditionalGeneration, AutoProcessor

from .forms import RegisterForm, UploadForm
from .models import UploadedImage, SearchHistory
from .spotify_utils import get_spotify_tracks


# ----------------------
# Helper: Generate AI music
# ----------------------
def generate_music(text, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    try:
        processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
        model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
        inputs = processor(text=text, return_tensors="pt")
        with torch.no_grad():
            generated_audio = model.generate(**inputs, max_duration=10.0)
        sf.write(output_file, generated_audio.squeeze().cpu().numpy(), samplerate=16000)
    except Exception as e:
        print(f"MusicGen model failed: {e}")
        # fallback to silent audio file
        sf.write(output_file, [0.0] * 16000, samplerate=16000)
    return output_file


# ----------------------
# Authentication Views
# ----------------------
def home(request):
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'ai_app/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('upload_image')
        else:
            error = "Invalid username or password"
            return render(request, 'ai_app/login.html', {'error': error})
    return render(request, 'ai_app/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ----------------------
# Upload Image View
# ----------------------
@login_required
def upload_image(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded = form.save(commit=False)
            uploaded.user = request.user
            uploaded.mood = random.choice(['Happy', 'Sad', 'Calm', 'Excited', 'Angry'])
            uploaded.save()
            return redirect('music_generation')
    else:
        form = UploadForm()
    return render(request, 'ai_app/upload.html', {'form': form})


# ----------------------
# Music Generation + Spotify + Search History
# ----------------------
@login_required
def music_generation_view(request):
    mood = None
    sentiment = None
    spotify_tracks = []
    generated_audio_url = None

    if request.method == 'POST':
        text_input = request.POST.get('text_input', '').strip()
        language = request.POST.get('language', 'English')
        song_type = request.POST.get('song_type', 'Pop')

        # --- Sentiment & Mood Detection ---
        polarity = TextBlob(text_input).sentiment.polarity
        if polarity > 0.1:
            sentiment = "Positive"
            mood = "Happy"
        elif polarity < -0.1:
            sentiment = "Negative"
            mood = "Sad"
        else:
            sentiment = "Neutral"
            mood = "Calm"

        # --- Spotify Recommendations ---
        spotify_tracks = get_spotify_tracks(mood, song_type, language, limit=5)

        # --- Save Search History ---
        SearchHistory.objects.create(
            user=request.user,
            mood=mood,
            sentiment=sentiment,
            language=language,
            song_type=song_type,
            search_text=text_input,
            created_at=timezone.now()
        )

        # --- Generate AI Music ---
        unique_filename = f"music_{request.user.id}_{uuid.uuid4().hex}.wav"
        output_file = os.path.join(settings.MEDIA_ROOT, unique_filename)
        generate_music(text_input, output_file)
        generated_audio_url = f"{settings.MEDIA_URL}{unique_filename}"

    # --- Fetch past search history ---
    history = SearchHistory.objects.filter(user=request.user).order_by('-created_at')

    return render(request, "ai_app/music_generation.html", {
        "mood": mood,
        "sentiment": sentiment,
        "spotify_tracks": spotify_tracks,
        "generated_audio_url": generated_audio_url,
        "history": history,
    })
