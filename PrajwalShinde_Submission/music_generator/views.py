from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from transformers import pipeline
import numpy as np
import soundfile as sf
import os

from .serializers import (
    RegisterSerializer, LoginSerializer, HistorySerializer,
    MusicRequestSerializer, MusicResponseSerializer
)
from .models import GenerationHistory

print("\n" + "="*70)
print("🔄 LOADING MODELS")
print("="*70)

sentiment_model = None

try:
    print("📥 Loading Sentiment...")
    sentiment_model = pipeline(
        "sentiment-analysis",
        model="cardiffnlp/twitter-roberta-base-sentiment-latest"
    )
    print("✅ Sentiment Model Ready!")
except Exception as e:
    print(f"❌ Error: {e}")

print("="*70)
print("✨ Server Ready!\n")


# ============ REGISTER API ============

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'message': '✅ Registered!',
                'username': user.username,
                'token': token.key,
            }, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# ============ LOGIN API ============

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'message': '✅ Login OK!',
            'username': user.username,
            'token': token.key,
        }, status=status.HTTP_200_OK)


# ============ MUSIC GENERATION API ============

class MusicGenerationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        print(f"\n🎵 GENERATE MUSIC - User: {request.user}")
        
        serializer = MusicRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        text = serializer.validated_data['text']
        print(f"   Text: {text}")
        
        try:
            # SENTIMENT ONLY (simple and reliable)
            print("   🔍 Analyzing...")
            if sentiment_model is None:
                sentiment = 'positive'
                mood = 'joy'
            else:
                try:
                    result = sentiment_model(text)
                    sentiment = result['label'].lower() if result else 'positive'
                except:
                    sentiment = 'positive'
                
                # Map sentiment to mood
                mood_map = {
                    'positive': 'joy',
                    'negative': 'sadness',
                    'neutral': 'neutral'
                }
                mood = mood_map.get(sentiment, 'neutral')
            
            print(f"   ✓ Sentiment: {sentiment}, Mood: {mood}")
            
            # Generate audio
            print("   🎵 Generating audio...")
            audio_data, sr = generate_music_from_mood(mood)
            
            # Save audio
            print("   💾 Saving...")
            os.makedirs("media", exist_ok=True)
            filename = f"{mood}_{sentiment}_20s.wav"
            sf.write(f"media/{filename}", audio_data, sr)
            
            # Save to database
            print("   📝 Saving to history...")
            GenerationHistory.objects.create(
                user=request.user,
                input_text=text,
                mood=mood,
                sentiment=sentiment,
                audio_file=filename
            )
            
            print("   ✅ SUCCESS!")
            return Response({
                "mood": mood,
                "sentiment": sentiment,
                "audio_file": filename,
                "message": "✨ Success!"
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ============ HISTORY API ============

class UserHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        print(f"\n📜 HISTORY - User: {request.user}")
        
        history = GenerationHistory.objects.filter(user=request.user)
        serializer = HistorySerializer(history, many=True)
        
        return Response({
            'username': request.user.username,
            'count': history.count(),
            'results': serializer.data
        }, status=status.HTTP_200_OK)


# ============ MUSIC GENERATION FUNCTION ============

def generate_music_from_mood(mood):
    """Generate audio based on mood"""
    mood_patterns = {
        'joy': ([523, 659, 784, 1046], [0.4, 0.4, 0.4, 0.4]),
        'anger': ([220, 220, 330, 440], [0.5, 0.5, 0.5, 0.5]),
        'sadness': ([220, 246, 261, 293], [0.6, 0.6, 0.6, 0.6]),
        'fear': ([440, 392, 349, 330], [0.5, 0.5, 0.5, 0.5]),
        'love': ([392, 440, 494, 523], [0.4, 0.4, 0.4, 0.4]),
        'surprise': ([523, 784, 988, 1319], [0.3, 0.3, 0.3, 0.3]),
        'neutral': ([440, 440, 440, 440], [0.5, 0.5, 0.5, 0.5])
    }
    
    frequencies, durations = mood_patterns.get(mood, mood_patterns['neutral'])
    sr = 22050
    song = np.array([], dtype=np.float32)
    loop_time = sum(durations)
    repeat_count = int(20 // loop_time)
    
    for _ in range(repeat_count):
        for freq, dur in zip(frequencies, durations):
            freq *= np.random.uniform(0.98, 1.02)
            t = np.linspace(0, dur, int(sr * dur), False)
            tone = 0.5 * np.sin(2 * np.pi * freq * t)
            song = np.concatenate((song, tone))
    
    if len(song) / sr < 20:
        remaining = 20 - (len(song) / sr)
        t = np.linspace(0, remaining, int(sr * remaining), False)
        tone = 0.5 * np.sin(2 * np.pi * frequencies[-1] * t)
        song = np.concatenate((song, tone))
    
    return song, sr
