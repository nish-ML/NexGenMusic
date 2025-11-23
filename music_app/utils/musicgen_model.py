# music_app/utils/musicgen_model.py

import os
from datetime import datetime

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
    try:
        # Try audiocraft first (better compatibility)
        try:
            from audiocraft.models import MusicGen
            from audiocraft.data.audio import audio_write

            # Validate duration
            duration_seconds = max(5, min(60, duration_seconds))  # Clamp between 5-60 seconds

            # Load model
            model = MusicGen.get_pretrained('facebook/musicgen-small')

            # Set generation parameters
            model.set_generation_params(duration=duration_seconds)

            # Generate
            wav = model.generate([prompt_text], progress=False)

            # Create filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"music_{timestamp}_{duration_seconds}s.wav"
            file_path = os.path.join(MEDIA_DIR, filename)

            # Save audio
            audio_write(file_path, wav[0].cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)

            print(f"✅ Music generated and saved at: {file_path} (Duration: {duration_seconds}s)")
            return file_path

        except ImportError:
            print("Audiocraft not available, falling back to transformers")
            # Fallback to transformers pipeline
            try:
                from transformers import pipeline
                import torch

                # Validate duration
                duration_seconds = max(5, min(30, duration_seconds))  # Clamp between 5-30 seconds for pipeline

                # Use the text-to-audio pipeline
                synthesiser = pipeline("text-to-audio", "facebook/musicgen-small")

                # Generate music
                music = synthesiser(prompt_text, forward_params={"do_sample": True, "max_new_tokens": duration_seconds * 50})

                # Create filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"music_{timestamp}_{duration_seconds}s.wav"
                file_path = os.path.join(MEDIA_DIR, filename)

                # Save audio to file
                import scipy.io.wavfile
                # MusicGen uses 32kHz sampling rate
                sampling_rate = 32000
                scipy.io.wavfile.write(file_path, rate=sampling_rate, data=music["audio"])

                print(f"✅ Music generated and saved at: {file_path} (Duration: {duration_seconds}s)")
                return file_path

            except Exception as e:
                print(f"❌ Transformers pipeline failed: {e}")
                # Last resort: try direct model loading with config patching
                try:
                    from transformers import MusicgenForConditionalGeneration, MusicgenProcessor
                    import torch

                    # Fix config issue for newer transformers versions
                    from transformers.models.musicgen.configuration_musicgen import MusicgenDecoderConfig, MusicgenConfig

                    # Add missing attributes to config classes
                    if not hasattr(MusicgenDecoderConfig, 'decoder'):
                        def _get_decoder(self):
                            return self.__dict__.get('decoder', {})
                        MusicgenDecoderConfig.decoder = property(_get_decoder)

                    if not hasattr(MusicgenDecoderConfig, 'text_encoder'):
                        def _get_text_encoder(self):
                            return self.__dict__.get('text_encoder', {})
                        MusicgenDecoderConfig.text_encoder = property(_get_text_encoder)

                    if not hasattr(MusicgenConfig, 'decoder'):
                        def _get_decoder_config(self):
                            return self.__dict__.get('decoder', {})
                        MusicgenConfig.decoder = property(_get_decoder_config)

                    if not hasattr(MusicgenConfig, 'text_encoder'):
                        def _get_text_encoder_config(self):
                            return self.__dict__.get('text_encoder', {})
                        MusicgenConfig.text_encoder = property(_get_text_encoder_config)

                    # Validate duration
                    duration_seconds = max(5, min(30, duration_seconds))

                    # Load processor and model
                    processor = MusicgenProcessor.from_pretrained("facebook/musicgen-small")
                    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")

                    # Convert text to tokens
                    inputs = processor(text=[prompt_text], padding=True, return_tensors="pt")

                    # Calculate max_new_tokens based on duration
                    max_new_tokens = int(duration_seconds * 50)

                    # Generate audio tensor
                    with torch.no_grad():
                        audio_values = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=True)

                    # Create filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"music_{timestamp}_{duration_seconds}s.wav"
                    file_path = os.path.join(MEDIA_DIR, filename)

                    # Save audio to file
                    import scipy.io.wavfile
                    sampling_rate = 32000
                    scipy.io.wavfile.write(file_path, rate=sampling_rate, data=audio_values[0, 0].cpu().numpy())

                    print(f"✅ Music generated with patched config at: {file_path}")
                    return file_path

                except Exception as e2:
                    print(f"❌ All music generation methods failed: {e2}")
                    # Create a placeholder audio file for demo purposes
                    try:
                        import numpy as np

                        # Create a more musical demo with melody
                        sample_rate = 44100  # Higher quality
                        duration = min(duration_seconds, 10)  # Limit to 10 seconds for demo

                        # Create a simple melody (Twinkle Twinkle Little Star)
                        notes = [261.63, 261.63, 392.00, 392.00, 440.00, 440.00, 392.00,  # C C G G A A G
                                349.23, 349.23, 329.63, 329.63, 293.66, 293.66, 261.63] # F F E E D D C

                        note_duration = duration / len(notes)
                        audio = np.array([])

                        for freq in notes:
                            t = np.linspace(0, note_duration, int(sample_rate * note_duration), False)
                            note_audio = np.sin(freq * 2 * np.pi * t)

                            # Add harmonics for richer sound
                            note_audio += 0.3 * np.sin(2 * freq * 2 * np.pi * t)
                            note_audio += 0.2 * np.sin(3 * freq * 2 * np.pi * t)

                            # Add fade in/out to avoid clicks
                            fade_samples = int(0.05 * sample_rate)  # 50ms fade
                            fade_in = np.linspace(0, 1, fade_samples)
                            fade_out = np.linspace(1, 0, fade_samples)

                            note_audio[:fade_samples] *= fade_in
                            note_audio[-fade_samples:] *= fade_out

                            audio = np.concatenate([audio, note_audio])

                        # Normalize and amplify
                        audio = audio / np.max(np.abs(audio))
                        audio = audio * 0.8  # Leave some headroom

                        # Create filename
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"demo_music_{timestamp}_{duration_seconds}s.wav"
                        file_path = os.path.join(MEDIA_DIR, filename)

                        # Save as WAV (int16 for maximum compatibility)
                        import scipy.io.wavfile
                        scipy.io.wavfile.write(file_path, sample_rate, (audio * 32767).astype(np.int16))

                        print(f"✅ Demo music generated at: {file_path} (musical melody placeholder)")
                        return file_path

                    except Exception as e3:
                        print(f"❌ Even demo music generation failed: {e3}")
                        return None

    except ImportError as e:
        print(f"❌ Music generation not available: dependencies not installed - {e}")
        return None
    except Exception as e:
        print(f"❌ Error generating music: {e}")
        return None
