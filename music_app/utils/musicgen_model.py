# music_app/utils/musicgen_model.py

from transformers import AutoProcessor, MusicgenForConditionalGeneration
import torch
import os
from datetime import datetime

# Lazy loading of model and processor
processor = None
model = None

# Make sure media directory exists
MEDIA_DIR = os.path.join(os.getcwd(), "media")
os.makedirs(MEDIA_DIR, exist_ok=True)

def generate_music(prompt_text, duration_seconds=30):
    """
    Generate a music file based on the text prompt using MusicGen model.
    Args:
        prompt_text: Text description of the music
        duration_seconds: Duration in seconds (5-60 seconds supported)
    Returns the file path of the generated music.
    """
    global processor, model
    try:
        # Lazy load models if not already loaded
        if processor is None:
            processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
        if model is None:
            model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")

        # Validate duration
        duration_seconds = max(5, min(60, duration_seconds))  # Clamp between 5-60 seconds

        # Convert text to tokens
        inputs = processor(
            text=[prompt_text],
            padding=True,
            return_tensors="pt"
        )

        # Calculate max_new_tokens based on duration
        # MusicGen generates ~50 tokens per second at 32kHz
        # Adjust for better duration accuracy - use slightly more tokens
        max_new_tokens = int(duration_seconds * 55)

        # Generate audio tensor
        audio_values = model.generate(**inputs, max_new_tokens=max_new_tokens)

        # Create filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"music_{timestamp}_{duration_seconds}s.wav"
        file_path = os.path.join(MEDIA_DIR, filename)

        # Save audio to file
        import scipy.io.wavfile
        sampling_rate = model.config.audio_encoder.sampling_rate
        scipy.io.wavfile.write(file_path, rate=sampling_rate, data=audio_values[0, 0].cpu().numpy())

        print(f"✅ Music generated and saved at: {file_path} (Duration: {duration_seconds}s)")
        return file_path

    except Exception as e:
        print(f"❌ Error generating music: {e}")
        return None
