import os
import torch
import joblib
import json
import random
import numpy as np
import wave
import struct
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import GeneratedMusic
from .serializers import GeneratedMusicSerializer
from enhanced_train_model import EnhancedMoodClassifier

# -------------------- MODEL LOADING --------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vectorizer = joblib.load(os.path.join(BASE_DIR, 'tfidf_vectorizer.pkl'))
label_encoder = joblib.load(os.path.join(BASE_DIR, 'label_encoder.pkl'))
model_info = json.load(open(os.path.join(BASE_DIR, 'training_info.json')))
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

input_size = model_info['vocabulary_size']
n_classes = len(model_info['classes'])
model = EnhancedMoodClassifier(input_size=input_size, n_classes=n_classes)
model.load_state_dict(torch.load(os.path.join(BASE_DIR, 'enhanced_mood_model.pth'), map_location=device))
model.eval()


# -------------------- PREDICT MOOD VIEW --------------------
class PredictMoodView(APIView):
    def post(self, request):
        text = request.data.get('text', '').strip()
        user = request.user if request.user.is_authenticated else None

# Attach default user automatically if anonymous
        if user is None or not user.is_authenticated:
            from django.contrib.auth.models import User
            user = User.objects.first()  # Assign first user in DB (like ID=1)


        if not text:
            return Response({'error': 'No text provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Vectorize input text
        features = vectorizer.transform([text]).toarray().flatten()
        features_tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0)

        with torch.no_grad():
            outputs = model(features_tensor.to(device))
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            predicted_class = torch.argmax(outputs, dim=1)
            mood = label_encoder.inverse_transform(predicted_class.cpu().numpy())[0]
            confidence = probabilities[0][predicted_class].item()

        # ---------------- EMOTIONAL MUSIC GENERATION ----------------
        music_path = os.path.join(settings.MEDIA_ROOT, 'generated_music')
        os.makedirs(music_path, exist_ok=True)
        filename = f"{mood}_{random.randint(1000,9999)}.wav"
        file_path = os.path.join(music_path, filename)

        sample_rate = 44100
        duration = 35  # total seconds

        # Emotion-based tone characteristics
        tone_profiles = {
            "happy": {
                "base_freqs": [440, 494, 523, 587, 659, 698, 784],  # major scale
                "volume": 0.7,
                "pattern": [0.4, 0.6, 0.5, 0.3, 0.7],
            },
            "sad": {
                "base_freqs": [220, 247, 262, 294, 330],  # minor scale
                "volume": 0.5,
                "pattern": [0.8, 0.9, 1.0, 0.6],
            },
            "angry": {
                "base_freqs": [400, 450, 500, 550, 600],  # harsh jumps
                "volume": 0.9,
                "pattern": [0.2, 0.3, 0.4],
            },
            "fear": {
                "base_freqs": [300, 330, 370, 400, 420],  # eerie oscillations
                "volume": 0.6,
                "pattern": [0.5, 0.4, 0.6, 0.5],
            },
            "neutral": {
                "base_freqs": [350, 370, 392, 415, 440],
                "volume": 0.6,
                "pattern": [0.5, 0.5, 0.5, 0.5],
            },
        }

        profile = tone_profiles.get(mood.lower(), tone_profiles["neutral"])
        total_samples = int(sample_rate * duration)
        music_data = np.zeros(total_samples)

        # Compose emotional melody dynamically
        position = 0
        while position < total_samples:
            freq = random.choice(profile["base_freqs"])
            note_duration = random.choice(profile["pattern"]) * 1.0  # seconds per note
            samples_per_note = int(sample_rate * note_duration)
            if position + samples_per_note > total_samples:
                samples_per_note = total_samples - position

            t = np.linspace(0, note_duration, samples_per_note, endpoint=False)

            # Emotion-based sound style
            if mood.lower() == "happy":
                tone = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(2 * np.pi * (freq * 2) * t)
            elif mood.lower() == "sad":
                tone = np.sin(2 * np.pi * freq * t) * np.exp(-t * 2)  # fading sadness
            elif mood.lower() == "angry":
                tone = np.sign(np.sin(2 * np.pi * freq * t))  # distorted harshness
            elif mood.lower() == "fear":
                tremble = np.sin(2 * np.pi * 6 * t)  # trembling effect
                tone = np.sin(2 * np.pi * (freq + 15 * tremble) * t)
            else:
                tone = np.sin(2 * np.pi * freq * t)  # calm, neutral

            # Apply volume
            tone = tone * profile["volume"]

            # Write into final buffer
            music_data[position:position + samples_per_note] = tone
            position += samples_per_note

        # Normalize & export
        music_data = np.int16(music_data / np.max(np.abs(music_data)) * 32767)
        with wave.open(file_path, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(struct.pack('<' + ('h' * len(music_data)), *music_data))

        # ---------------- SAVE RECORD ----------------
        record = GeneratedMusic.objects.create(
            user=user,
            prompt=text,
            mood=mood,
            confidence=round(confidence, 4),
            audio_file=f"generated_music/{filename}",
            ai_metadata={
                "probabilities": probabilities.cpu().numpy().tolist(),
                "classes": model_info["classes"]
            }
        )

        return Response({
            "mood": mood,
            "confidence": round(confidence * 100, 2),
            "music_file": record.audio_file.url if record.audio_file else None,
            "id": record.id
        })


# -------------------- USER MANAGEMENT --------------------
class UserViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email", "")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password, email=email)
        return Response({"message": "Registered successfully", "user_id": user.id}, status=201)

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"message": "Login successful", "user_id": user.id})
        return Response({"error": "Invalid credentials"}, status=401)


# -------------------- HISTORY VIEW --------------------
class HistoryView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            history = GeneratedMusic.objects.filter(user=user).order_by('-created_at')
            serializer = GeneratedMusicSerializer(history, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


