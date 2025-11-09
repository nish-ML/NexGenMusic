import torch
import random
import soundfile as sf
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    AutoProcessor,
    MusicgenForConditionalGeneration
)
from django.core.files.base import ContentFile
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import MusicTrack
from .serializers import MusicTrackSerializer, RegisterSerializer, LoginSerializer


# ======================================================
# Load Hugging Face Models (once on server startup)
# ======================================================
print("🚀 Loading Hugging Face models...")

# Sentiment model
sent_tokenizer = AutoTokenizer.from_pretrained(
    "distilbert-base-uncased-finetuned-sst-2-english")
sent_model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased-finetuned-sst-2-english"
)

# MusicGen model
music_processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
music_model = MusicgenForConditionalGeneration.from_pretrained(
    "facebook/musicgen-small")

device = "cuda" if torch.cuda.is_available() else "cpu"
sent_model = sent_model.to(device)
music_model = music_model.to(device)

print(f"✅ Models loaded on {device}\n")


# ======================================================
# Helper Functions
# ======================================================

def predict_sentiment(text: str) -> str:
    inputs = sent_tokenizer(text, return_tensors="pt",
                            truncation=True, padding=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = sent_model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        label = torch.argmax(probs, dim=1).item()

    return "positive" if label == 1 else "negative"


def predict_mood(sentiment: str) -> str:
    mood_map = {
        "positive": ["happy", "uplifting", "energetic"],
        "negative": ["sad", "melancholic", "calm"]
    }
    return random.choice(mood_map.get(sentiment, ["neutral"]))


def generate_music(prompt: str, duration: int = 30):
    """Generate music using facebook/musicgen-small."""
    inputs = music_processor(
        text=[prompt], padding=True, return_tensors="pt").to(device)
    with torch.no_grad():
        audio_values = music_model.generate(
            **inputs, max_new_tokens=duration * 175)
    audio_array = audio_values[0, 0].cpu().numpy()
    sampling_rate = music_model.config.audio_encoder.sampling_rate
    return audio_array, sampling_rate


# ======================================================
# ViewSets
# ======================================================

class UserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "message": "User registered successfully.",
                "token": token.key,
                "user_id": user.id
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": token.key, "user_id": user.id})
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenerateMusicViewSet(viewsets.ModelViewSet):
    queryset = MusicTrack.objects.all()
    serializer_class = MusicTrackSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='generate')
    def generate_music_api(self, request):
        prompt = request.data.get("prompt")
        duration = int(request.data.get("duration", 8))

        if not prompt:
            return Response({"error": "Prompt is required"}, status=status.HTTP_400_BAD_REQUEST)

        sentiment = predict_sentiment(prompt)
        mood = predict_mood(sentiment)
        audio_array, sample_rate = generate_music(prompt, duration=duration)

        # Save the generated music to /media/music_tracks/
        file_name = f"{mood}_{random.randint(1000, 9999)}.wav"
        import os

        # Ensure directory exists before writing
        os.makedirs("media/music_tracks", exist_ok=True)

        file_path = os.path.join("media/music_tracks", file_name)
        sf.write(file_path, audio_array, sample_rate)

        music_track = MusicTrack.objects.create(
            user=request.user,
            title=f"{mood.title()} Track",
            prompt=prompt,
            mood=mood,
            sentiment=sentiment,
            generated_music=file_path.replace("media/", "")
        )

        serializer = MusicTrackSerializer(music_track)
        return Response({
            "message": "Music generated successfully!",
            "sentiment": sentiment,
            "mood": mood,
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='history')
    def history(self, request):
        user_id = request.query_params.get("user_id")
        if user_id:
            queryset = MusicTrack.objects.filter(
                user_id=user_id).order_by("-created_at")
        else:
            queryset = MusicTrack.objects.filter(
                user=request.user).order_by("-created_at")
        serializer = MusicTrackSerializer(queryset, many=True)
        return Response(serializer.data)
