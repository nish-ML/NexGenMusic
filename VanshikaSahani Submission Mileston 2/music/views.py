from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings

from rest_framework import viewsets
from .serializers import MusicRecordSerializer
from .forms import RegisterForm, LoginForm
from .models import MusicRecord

from transformers import pipeline, MusicgenForConditionalGeneration, AutoProcessor
import torch, os, requests, base64
from scipy.io.wavfile import write
from datetime import datetime

# Device setup
device = "cuda" if torch.cuda.is_available() else "cpu"
print("🖥️ Using device:", device)

# Global caches
emotion_classifier = None
sentiment_classifier = None
music_processor = None
music_model = None

# Mood-based prompts
mood_prompts = {
    "joy": "upbeat happy pop music with bright energy",
    "sadness": "slow emotional piano music",
    "anger": "intense rock music with heavy drums",
    "fear": "dark cinematic tension music",
    "love": "romantic acoustic guitar melody",
    "surprise": "playful quirky music",
    "calm": "soothing ambient background"
}

# Load models (only once)
def get_models():
    global emotion_classifier, sentiment_classifier, music_processor, music_model

    if emotion_classifier is None:
        emotion_classifier = pipeline(
            "text-classification",
            model="bhadresh-savani/distilbert-base-uncased-emotion",
            top_k=None
        )

    if sentiment_classifier is None:
        sentiment_classifier = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )

    if music_model is None or music_processor is None:
        music_processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
        music_model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small").to(device)
        if device == "cuda":
            music_model = music_model.half()

# Spotify API token generator
def get_spotify_token():
    auth_str = f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        headers={"Authorization": f"Basic {b64_auth_str}"}
    )
    return response.json().get("access_token") if response.status_code == 200 else None

# API Viewset
class MusicRecordViewSet(viewsets.ModelViewSet):
    queryset = MusicRecord.objects.all().order_by('-created_at')
    serializer_class = MusicRecordSerializer

# Register view
def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                messages.warning(request, "User already exists. Please log in.")
                return redirect('login')

            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()

    return render(request, 'music/register.html', {'form': form})

# Login view
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'music/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

# Home view (Music history)
@login_required(login_url='login')
def index_view(request):
    past_records = MusicRecord.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'music/index.html', {"past_records": past_records})

# Music generation + Spotify integration
@login_required(login_url='login')
def generate_music(request):
    if request.method == "POST":
        get_models()
        user_text = request.POST.get("mood", "").strip().lower()
        if not user_text:
            return render(request, "music/index.html", {"error": "Please enter a mood or description."})

        # Emotion detection
        if any(word in user_text for word in ["sad", "upset", "depressed", "down"]):
            detected_mood, confidence = "sadness", 0.99
        else:
            emotion_result = emotion_classifier(user_text)[0][0]
            detected_mood = emotion_result.get("label", "calm").lower()
            confidence = emotion_result.get("score", 0.0)

        # Sentiment analysis
        sent_pred = sentiment_classifier(user_text)[0]
        sentiment = sent_pred.get("label", "neutral")

        # Generate AI music
        prompt = mood_prompts.get(detected_mood, "background ambient music")
        with torch.no_grad():
            inputs = music_processor(text=prompt, return_tensors="pt").to(device)
            audio_values = music_model.generate(**inputs, max_new_tokens=512)
        audio_numpy = audio_values[0, 0].detach().cpu().float().numpy()

        # Save to static folder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        relative_path = f"generated_music_{timestamp}.wav"
        output_path = f"static/{relative_path}"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        write(output_path, rate=32000, data=audio_numpy)

        # Save to DB
        MusicRecord.objects.create(
            user=request.user,
            user_input=user_text,
            mood=detected_mood,
            confidence=round(confidence, 2),
            sentiment=sentiment,
            audio_file=output_path
        )

        # Spotify recommendations
        spotify_token = get_spotify_token()
        english_tracks, hindi_tracks = [], []

        if spotify_token:
            headers = {"Authorization": f"Bearer {spotify_token}"}
            for market, track_list in [("US", english_tracks), ("IN", hindi_tracks)]:
                resp = requests.get(
                    f"https://api.spotify.com/v1/search?q={detected_mood} music&type=track&market={market}&limit=5",
                    headers=headers
                )
                if resp.status_code == 200:
                    for track in resp.json().get("tracks", {}).get("items", []):
                        track_list.append({
                            "name": track["name"],
                            "artist": track["artists"][0]["name"],
                            "album_image": track["album"]["images"][0]["url"],
                            "spotify_url": track["external_urls"]["spotify"],
                            "embed_url": f"https://open.spotify.com/embed/track/{track['id']}"
                        })

        past_records = MusicRecord.objects.filter(user=request.user).order_by('-created_at')
        return render(request, "music/result.html", {
            "mood": detected_mood,
            "confidence": round(confidence, 2),
            "sentiment": sentiment,
            "user_text": user_text,
            "audio_file": relative_path,
            "english_tracks": english_tracks,
            "hindi_tracks": hindi_tracks,
            "past_records": past_records
        })
    return redirect('index')
