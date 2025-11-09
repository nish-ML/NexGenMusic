import os
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .ml import generate_music, predict_sentiment_and_mood
from .models import GenerationHistory
from .serializers import RegisterSerializer, GenerationHistorySerializer


class RegisterView(generics.CreateAPIView):
	queryset = User.objects.all()
	permission_classes = [permissions.AllowAny]
	serializer_class = RegisterSerializer


class GenerateView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request):
		prompt = request.data.get("prompt", "").strip()
		try:
			duration_sec = int(request.data.get("duration", 10))
		except Exception:
			duration_sec = 10
		if not prompt:
			return Response({"detail": "prompt is required"}, status=status.HTTP_400_BAD_REQUEST)

		mood, sentiment = predict_sentiment_and_mood(prompt)

		media_dir = os.path.join(settings.MEDIA_ROOT, "generated")
		os.makedirs(media_dir, exist_ok=True)
		filename = f"{uuid.uuid4().hex}.wav"
		output_path = os.path.join(media_dir, filename)

		generate_music(prompt, duration_sec, output_path)

		history = GenerationHistory.objects.create(
			user=request.user,
			prompt=prompt,
			mood=mood,
			sentiment=sentiment,
			audio_file=f"generated/{filename}",
			duration_sec=duration_sec,
		)

		serializer = GenerationHistorySerializer(history)
		return Response(serializer.data, status=status.HTTP_201_CREATED)


class HistoryView(generics.ListAPIView):
	serializer_class = GenerationHistorySerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return GenerationHistory.objects.filter(user=self.request.user)


