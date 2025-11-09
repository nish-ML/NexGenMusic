from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from .models import GeneratedMusic
import os, time, wave, math, struct

analyzer = SentimentIntensityAnalyzer()

# ----------------- Pages -----------------
def login_page(request):
    return render(request, "login.html")

def register_page(request):
    return render(request, "register.html")

def dashboard(request):
    return render(request, "dashboard.html")

# ----------------- API Register/Login -----------------
@csrf_exempt
def api_register(request):
    import json
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")
    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "User already exists"})
    User.objects.create_user(username=username, password=password)
    return JsonResponse({"success": True})

@csrf_exempt
def api_login(request):
    import json
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")
    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({"error": "Invalid Credentials"})
    login(request, user)
    return JsonResponse({"success": True, "username": user.username})

# ----------------- Mood Detection -----------------
def detect_mood_vader(prompt):
    if not prompt:
        return "neutral", "Neutral", 0.0

    vs = analyzer.polarity_scores(prompt)
    compound_score = vs['compound']

    sentiment = ''
    mood = 'CALM'
    if compound_score >= 0.5:
        sentiment = 'Positive'
        mood = 'HAPPY'
    elif compound_score > 0.1:
        sentiment = 'Slightly Positive'
        mood = 'MOTIVATIONAL'
    elif compound_score <= -0.5:
        sentiment = 'Negative'
        mood = 'SAD'
    elif compound_score < -0.1:
        sentiment = 'Slightly Negative'
        mood = 'FEAR'
    else:
        sentiment = 'Neutral'
        mood = 'CALM'

    return mood, sentiment, compound_score

# ----------------- WAV Generation -----------------
def generate_wav(path, mood):
    duration = 20
    sample_rate = 44100
    amplitude = 18000
    freq_map = {
        "HAPPY": 550,
        "SAD": 300,
        "ANGRY": 800,
        "CALM": 220,
        "ROMANTIC": 440,
        "MOTIVATIONAL": 650,
        "FEAR": 350,
        "NEUTRAL": 500,
    }
    freq = freq_map.get(mood.upper(), 500)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        for i in range(int(sample_rate * duration)):
            value = int(amplitude * math.sin(2 * math.pi * freq * (i / sample_rate)))
            data = struct.pack("<h", value)
            w.writeframesraw(data)

# ----------------- Generate Music API -----------------
@method_decorator(csrf_exempt, name='dispatch')
class GenerateMusicAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        prompt = request.data.get("prompt", "")
        mood, sentiment, score = detect_mood_vader(prompt)

        out_dir = os.path.join(settings.MEDIA_ROOT, "generated_music")
        os.makedirs(out_dir, exist_ok=True)
        filename = f"{int(time.time())}.wav"
        filepath = os.path.join(out_dir, filename)
        generate_wav(filepath, mood)

        user = request.user if request.user.is_authenticated else None
        GeneratedMusic.objects.create(
            user=user,
            prompt=prompt,
            mood=mood,
            audio_file=f"generated_music/{filename}",
        )

        return Response({
            "mood": mood,
            "sentiment": sentiment,
            "sentiment_score": round(score, 4),
            "file_url": request.build_absolute_uri(settings.MEDIA_URL + "generated_music/" + filename)
        })

# ----------------- Music History API -----------------
@login_required
def music_history(request):
    user = request.user
    history = GeneratedMusic.objects.filter(user=user).order_by('-id')  # latest first
    data = []
    for music in history:
        data.append({
            "prompt": music.prompt,
            "mood": music.mood,
            "file_url": request.build_absolute_uri(music.audio_file.url),
            "created_at": music.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        })
    return JsonResponse({"history": data})
