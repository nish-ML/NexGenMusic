import torch
import scipy.io.wavfile as wavfile
from transformers import (
    AutoProcessor,
    MusicgenForConditionalGeneration,
    pipeline
)
from pathlib import Path

# ============================
# MODEL INITIALIZATION
# ============================

device = "cuda" if torch.cuda.is_available() else "cpu"

print("🎵 Loading MusicGen and Sentiment Models...")

# Music generation model
music_processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
music_model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small").to(device)

# Sentiment analysis model (lightweight)
sentiment_model = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

# Where to save generated files
MEDIA_ROOT = Path("media/music")
MEDIA_ROOT.mkdir(parents=True, exist_ok=True)

print("✅ Models loaded successfully.")


# ============================
# SENTIMENT + MOOD PREDICTION
# ============================

def analyze_sentiment_and_mood(text: str):
    """Predict sentiment and derive mood."""
    sentiment = sentiment_model(text)[0]
    label = sentiment["label"].lower()
    score = sentiment["score"]

    # Map sentiment to mood
    if "positive" in label:
        mood = "happy"
    elif "negative" in label:
        mood = "sad"
    else:
        mood = "calm"

    return {
        "sentiment": label,
        "score": round(score, 3),
        "predicted_mood": mood
    }


# ============================
# MUSIC GENERATION
# ============================

def generate_music(prompt: str, mood: str = "neutral", duration: int = 10, filename: str = "output"):
    """Generate music from a text prompt and mood using MusicGen."""
    try:
        duration = min(max(int(duration), 1), 30)
        max_new_tokens = int(duration * 50)

        final_prompt = f"{prompt}. The mood of the music should be {mood}."

        inputs = music_processor(text=[final_prompt], padding=True, return_tensors="pt").to(device)

        with torch.no_grad():
            audio_values = music_model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                guidance_scale=3.0
            )

        sampling_rate = music_model.config.audio_encoder.sampling_rate
        audio_array = audio_values[0, 0].cpu().numpy()

        # Save to disk
        output_path = MEDIA_ROOT / f"{filename}.wav"
        wavfile.write(output_path, rate=sampling_rate, data=audio_array)

        return {
            "filename": f"{filename}.wav",
            "sampling_rate": sampling_rate,
            "length_seconds": len(audio_array) / sampling_rate,
            "file_path": str(output_path),
            "relative_path": f"/media/music/{filename}.wav"
        }

    except Exception as e:
        raise RuntimeError(f"Music generation failed: {e}")


# ============================
# MASTER FUNCTION
# ============================

def process_music_request(prompt: str, duration: int = 30, filename: str = "output"):
    """Complete pipeline: sentiment → mood → music generation."""
    analysis = analyze_sentiment_and_mood(prompt)
    mood = analysis["predicted_mood"]

    result = generate_music(prompt, mood, duration, filename)

    return {
        **analysis,
        **result
    }
