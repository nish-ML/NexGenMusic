import os
from functools import lru_cache
from typing import Dict, Tuple

import numpy as np
import soundfile as sf
from transformers import pipeline


MOOD_LABELS = [
	"admiration",
	"amusement",
	"anger",
	"annoyance",
	"approval",
	"caring",
	"confusion",
	"curiosity",
	"desire",
	"disappointment",
	"disgust",
	"excitement",
	"fear",
	"gratitude",
	"grief",
	"joy",
	"love",
	"nervousness",
	"optimism",
	"pride",
	"realization",
	"relief",
	"remorse",
	"sadness",
	"surprise",
	"neutral",
]


@lru_cache(maxsize=1)
def get_musicgen_pipe():
	return pipeline("text-to-audio", model="facebook/musicgen-small")


@lru_cache(maxsize=1)
def get_sentiment_pipe():
	return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")


@lru_cache(maxsize=1)
def get_mood_pipe():
	# Smaller multi-label emotion classifier (go-emotions distilled)
	return pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)


def predict_sentiment_and_mood(prompt: str) -> Tuple[str, str]:
	sentiment = get_sentiment_pipe()(prompt)[0]["label"].lower()
	results = get_mood_pipe()(prompt)
	if isinstance(results, list) and results and isinstance(results[0], list):
		# top_k=None returns list of lists; take top label from first entry
		results = results[0]
	mood = max(results, key=lambda r: r["score"])["label"].lower()
	return mood, sentiment


def generate_music(prompt: str, duration_sec: int, output_path: str) -> Dict[str, str]:
	pipe = get_musicgen_pipe()
	result = pipe(prompt, forward_params={"do_sample": True, "guidance_scale": 4})
	# The pipeline may ignore duration; truncate/pad to requested duration if needed
	audio = np.asarray(result["audio"], dtype=np.float32)
	sr = result["sampling_rate"]
	target_len = int(duration_sec * sr)

	if audio.ndim == 1:
		if audio.shape[0] > target_len:
			audio = audio[:target_len]
		elif audio.shape[0] < target_len:
			audio = np.pad(audio, (0, target_len - audio.shape[0]))
	elif audio.ndim == 2:
		current_len = audio.shape[1]
		if current_len > target_len:
			audio = audio[:, :target_len]
		elif current_len < target_len:
			pad_width = ((0, 0), (0, target_len - current_len))
			audio = np.pad(audio, pad_width)
	else:
		# Collapse any unexpected dimensions (e.g., batch, channels, samples)
		audio = audio.reshape(-1, audio.shape[-1])
		current_len = audio.shape[1]
		if current_len > target_len:
			audio = audio[:, :target_len]
		elif current_len < target_len:
			pad_width = ((0, 0), (0, target_len - current_len))
			audio = np.pad(audio, pad_width)
		# mixdown to mono for writing
		audio = np.mean(audio, axis=0)

	if audio.ndim == 2:
		audio = audio.T  # soundfile expects (n_frames, n_channels)
	sf.write(output_path, audio, sr)
	return {"path": output_path, "sampling_rate": sr}


