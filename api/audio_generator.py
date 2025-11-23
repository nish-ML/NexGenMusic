"""
AI-Powered Audio Generation System
Generates 40-second audio clips based on detected mood and sentiment
"""

import numpy as np
import random
import os
from datetime import datetime

# Import required libraries with fallback
try:
    import soundfile as sf
    SOUNDFILE_AVAILABLE = True
except ImportError:
    SOUNDFILE_AVAILABLE = False
    sf = None

try:
    from scipy import signal
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    signal = None

class AudioGenerator:
    """
    Generate audio clips based on mood and sentiment analysis
    """
    
    def __init__(self):
        self.sample_rate = 44100
        self.duration = 40  # 40 seconds as requested
        self.output_dir = "generated_audio"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_mood_audio(self, mood, sentiment_score=0.0, intensity=0.5):
        """
        Generate a 40-second audio clip based on mood and sentiment
        
        Args:
            mood: Detected mood (happy, sad, energetic, etc.)
            sentiment_score: Sentiment polarity (-1 to 1)
            intensity: Emotion intensity (0 to 1)
            
        Returns:
            str: Path to generated audio file
        """
        # Generate base audio based on mood
        audio = self._generate_base_audio(mood, sentiment_score, intensity)
        
        # Apply mood-specific effects
        audio = self._apply_mood_effects(audio, mood, intensity)
        
        # Apply sentiment-based modulation
        audio = self._apply_sentiment_modulation(audio, sentiment_score)
        
        # Normalize and ensure proper length
        audio = self._normalize_audio(audio)
        
        # Save to file
        filename = self._save_audio(audio, mood, sentiment_score)
        
        return filename
    
    def _generate_base_audio(self, mood, sentiment_score, intensity):
        """
        Generate base audio waveform based on mood
        """
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration))
        
        # Mood-specific frequency and rhythm patterns
        mood_params = self._get_mood_parameters(mood, intensity)
        
        # Generate multiple layers
        audio = np.zeros_like(t)
        
        # Base melody layer
        melody = self._generate_melody(t, mood_params)
        audio += melody * 0.4
        
        # Harmony layer
        harmony = self._generate_harmony(t, mood_params)
        audio += harmony * 0.3
        
        # Rhythm layer
        rhythm = self._generate_rhythm(t, mood_params)
        audio += rhythm * 0.3
        
        return audio
    
    def _get_mood_parameters(self, mood, intensity):
        """
        Get audio generation parameters for specific mood
        """
        params = {
            'happy': {
                'base_freq': 440,  # A4
                'scale': [0, 2, 4, 5, 7, 9, 11],  # Major scale
                'tempo': 120 + (intensity * 40),
                'brightness': 0.8,
                'rhythm_complexity': 0.7
            },
            'sad': {
                'base_freq': 220,  # A3
                'scale': [0, 2, 3, 5, 7, 8, 10],  # Natural minor
                'tempo': 60 + (intensity * 20),
                'brightness': 0.3,
                'rhythm_complexity': 0.3
            },
            'energetic': {
                'base_freq': 523,  # C5
                'scale': [0, 2, 4, 5, 7, 9, 11],  # Major scale
                'tempo': 140 + (intensity * 60),
                'brightness': 0.9,
                'rhythm_complexity': 0.9
            },
            'calm': {
                'base_freq': 330,  # E4
                'scale': [0, 2, 4, 7, 9],  # Pentatonic
                'tempo': 70 + (intensity * 10),
                'brightness': 0.5,
                'rhythm_complexity': 0.2
            },
            'romantic': {
                'base_freq': 392,  # G4
                'scale': [0, 2, 4, 5, 7, 9, 11],  # Major scale
                'tempo': 80 + (intensity * 20),
                'brightness': 0.6,
                'rhythm_complexity': 0.4
            },
            'angry': {
                'base_freq': 146,  # D3
                'scale': [0, 1, 3, 5, 6, 8, 10],  # Harmonic minor
                'tempo': 130 + (intensity * 50),
                'brightness': 0.9,
                'rhythm_complexity': 0.8
            },
            'anxious': {
                'base_freq': 277,  # C#4
                'scale': [0, 1, 3, 4, 6, 8, 9],  # Diminished
                'tempo': 100 + (intensity * 30),
                'brightness': 0.4,
                'rhythm_complexity': 0.6
            }
        }
        
        return params.get(mood, params['calm'])
    
    def _generate_melody(self, t, params):
        """
        Generate melodic line based on mood parameters
        """
        base_freq = params['base_freq']
        scale = params['scale']
        tempo = params['tempo']
        
        # Create melody with scale notes
        melody = np.zeros_like(t)
        note_duration = 60 / tempo  # Duration of each note in seconds
        
        for i in range(int(self.duration / note_duration)):
            start_time = i * note_duration
            end_time = min((i + 1) * note_duration, self.duration)
            
            # Select random note from scale
            scale_degree = random.choice(scale)
            freq = base_freq * (2 ** (scale_degree / 12))
            
            # Generate note
            note_mask = (t >= start_time) & (t < end_time)
            if np.any(note_mask):  # Only process if there are samples in this time range
                envelope = self._generate_envelope(t[note_mask], note_duration)
                melody[note_mask] = np.sin(2 * np.pi * freq * (t[note_mask] - start_time)) * envelope
        
        return melody
    
    def _generate_harmony(self, t, params):
        """
        Generate harmonic accompaniment
        """
        base_freq = params['base_freq'] / 2  # Lower octave
        scale = params['scale']
        
        # Generate chord progression
        harmony = np.zeros_like(t)
        chord_duration = 4.0  # 4 seconds per chord
        
        for i in range(int(self.duration / chord_duration)):
            start_time = i * chord_duration
            end_time = min((i + 1) * chord_duration, self.duration)
            
            # Generate triad chord
            root_idx = random.randint(0, len(scale) - 1)
            third_idx = (root_idx + 2) % len(scale)
            fifth_idx = (root_idx + 4) % len(scale)
            
            chord_mask = (t >= start_time) & (t < end_time)
            if np.any(chord_mask):  # Only process if there are samples in this time range
                envelope = self._generate_envelope(t[chord_mask], chord_duration) * 0.5
                
                # Add chord tones
                for degree in [scale[root_idx], scale[third_idx], scale[fifth_idx]]:
                    freq = base_freq * (2 ** (degree / 12))
                    harmony[chord_mask] += np.sin(2 * np.pi * freq * (t[chord_mask] - start_time)) * envelope / 3
        
        return harmony
    
    def _generate_rhythm(self, t, params):
        """
        Generate rhythmic percussion elements
        """
        tempo = params['tempo']
        complexity = params['rhythm_complexity']
        
        rhythm = np.zeros_like(t)
        beat_duration = 60 / tempo
        
        for i in range(int(self.duration / beat_duration)):
            start_time = i * beat_duration
            
            # Add kick drum on beats 1 and 3
            if i % 4 in [0, 2]:
                kick = self._generate_kick(t, start_time, beat_duration)
                rhythm += kick
            
            # Add snare on beats 2 and 4
            if i % 4 in [1, 3]:
                snare = self._generate_snare(t, start_time, beat_duration)
                rhythm += snare
            
            # Add hi-hat based on complexity
            if random.random() < complexity:
                hihat = self._generate_hihat(t, start_time, beat_duration)
                rhythm += hihat
        
        return rhythm
    
    def _generate_envelope(self, t, duration):
        """
        Generate ADSR envelope for notes
        """
        attack = min(0.1, duration * 0.1)
        decay = min(0.2, duration * 0.2)
        sustain_level = 0.7
        release = min(0.3, duration * 0.3)
        
        envelope = np.ones_like(t)
        
        # Attack
        attack_mask = t < attack
        envelope[attack_mask] = t[attack_mask] / attack
        
        # Decay
        decay_mask = (t >= attack) & (t < attack + decay)
        envelope[decay_mask] = 1 - (1 - sustain_level) * (t[decay_mask] - attack) / decay
        
        # Release
        release_start = duration - release
        release_mask = t >= release_start
        envelope[release_mask] = sustain_level * (1 - (t[release_mask] - release_start) / release)
        
        return envelope
    
    def _generate_kick(self, t, start_time, duration):
        """
        Generate kick drum sound
        """
        kick_duration = min(0.2, duration)
        mask = (t >= start_time) & (t < start_time + kick_duration)
        
        if not np.any(mask):
            return np.zeros_like(t)
        
        t_kick = t[mask] - start_time
        envelope = np.exp(-t_kick * 20)  # Quick decay
        
        # Low frequency sine wave with pitch bend
        freq = 60 * np.exp(-t_kick * 10)
        kick = np.sin(2 * np.pi * freq * t_kick) * envelope
        
        result = np.zeros_like(t)
        result[mask] = kick
        return result * 0.3
    
    def _generate_snare(self, t, start_time, duration):
        """
        Generate snare drum sound
        """
        snare_duration = min(0.15, duration)
        mask = (t >= start_time) & (t < start_time + snare_duration)
        
        if not np.any(mask):
            return np.zeros_like(t)
        
        t_snare = t[mask] - start_time
        envelope = np.exp(-t_snare * 15)
        
        # White noise with tonal component
        noise = np.random.normal(0, 1, len(t_snare))
        tone = np.sin(2 * np.pi * 200 * t_snare)
        snare = (noise * 0.7 + tone * 0.3) * envelope
        
        result = np.zeros_like(t)
        result[mask] = snare
        return result * 0.2
    
    def _generate_hihat(self, t, start_time, duration):
        """
        Generate hi-hat sound
        """
        hihat_duration = min(0.05, duration)
        mask = (t >= start_time) & (t < start_time + hihat_duration)
        
        if not np.any(mask):
            return np.zeros_like(t)
        
        t_hihat = t[mask] - start_time
        envelope = np.exp(-t_hihat * 50)
        
        # High frequency noise
        noise = np.random.normal(0, 1, len(t_hihat))
        hihat = signal.butter(4, 8000, 'high', fs=self.sample_rate, output='sos')
        filtered_noise = signal.sosfilt(hihat, noise) * envelope
        
        result = np.zeros_like(t)
        result[mask] = filtered_noise
        return result * 0.1
    
    def _apply_mood_effects(self, audio, mood, intensity):
        """
        Apply mood-specific audio effects
        """
        if mood == 'happy':
            # Add brightness and reverb
            audio = self._add_reverb(audio, 0.3)
            audio = self._add_brightness(audio, intensity * 0.5)
        
        elif mood == 'sad':
            # Add low-pass filter and reverb
            audio = self._apply_lowpass(audio, 2000)
            audio = self._add_reverb(audio, 0.5)
        
        elif mood == 'energetic':
            # Add compression and distortion
            audio = self._add_compression(audio, 0.7)
            audio = self._add_distortion(audio, intensity * 0.3)
        
        elif mood == 'calm':
            # Add gentle reverb and low-pass
            audio = self._apply_lowpass(audio, 4000)
            audio = self._add_reverb(audio, 0.4)
        
        return audio
    
    def _apply_sentiment_modulation(self, audio, sentiment_score):
        """
        Modulate audio based on sentiment score
        """
        if sentiment_score > 0:
            # Positive sentiment: increase brightness and add subtle chorus
            audio = self._add_brightness(audio, sentiment_score * 0.3)
        elif sentiment_score < 0:
            # Negative sentiment: darken and add subtle distortion
            audio = self._apply_lowpass(audio, 3000 + sentiment_score * 1000)
        
        return audio
    
    def _add_reverb(self, audio, amount):
        """
        Add simple reverb effect
        """
        delay_samples = int(0.05 * self.sample_rate)  # 50ms delay
        delayed = np.pad(audio, (delay_samples, 0), mode='constant')[:-delay_samples]
        return audio + delayed * amount * 0.3
    
    def _add_brightness(self, audio, amount):
        """
        Add brightness using high-frequency emphasis
        """
        sos = signal.butter(2, 2000, 'high', fs=self.sample_rate, output='sos')
        bright = signal.sosfilt(sos, audio)
        return audio + bright * amount
    
    def _apply_lowpass(self, audio, cutoff):
        """
        Apply low-pass filter
        """
        sos = signal.butter(4, cutoff, 'low', fs=self.sample_rate, output='sos')
        return signal.sosfilt(sos, audio)
    
    def _add_compression(self, audio, ratio):
        """
        Simple compression effect
        """
        threshold = 0.5
        compressed = np.copy(audio)
        over_threshold = np.abs(audio) > threshold
        compressed[over_threshold] = np.sign(audio[over_threshold]) * (
            threshold + (np.abs(audio[over_threshold]) - threshold) / ratio
        )
        return compressed
    
    def _add_distortion(self, audio, amount):
        """
        Add subtle distortion
        """
        return np.tanh(audio * (1 + amount * 5)) / (1 + amount)
    
    def _normalize_audio(self, audio):
        """
        Normalize audio to prevent clipping
        """
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            audio = audio / max_val * 0.8  # Leave some headroom
        return audio
    
    def _save_audio(self, audio, mood, sentiment_score):
        """
        Save audio to file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{mood}_{sentiment_score:.2f}_{timestamp}.wav"
        filepath = os.path.join(self.output_dir, filename)
        
        if SOUNDFILE_AVAILABLE and sf is not None:
            # Save audio as WAV file
            sf.write(filepath, audio, self.sample_rate)
            return filepath
        else:
            # Fallback: save as text file with instructions
            txt_filepath = filepath.replace('.wav', '.txt')
            with open(txt_filepath, 'w') as f:
                f.write(f"Audio generated for mood: {mood}, sentiment: {sentiment_score:.2f}\n")
                f.write(f"Duration: {self.duration} seconds\n")
                f.write(f"Sample rate: {self.sample_rate} Hz\n")
                f.write("\nNote: soundfile library not available.\n")
                f.write("Install with: pip install soundfile\n")
            return txt_filepath
    
    def generate_audio_preview(self, mood, sentiment_score=0.0, intensity=0.5, duration=10):
        """
        Generate a shorter preview (10 seconds) for quick testing
        """
        original_duration = self.duration
        self.duration = duration
        
        try:
            filepath = self.generate_mood_audio(mood, sentiment_score, intensity)
            return filepath
        finally:
            self.duration = original_duration

# Global audio generator instance
_audio_generator = None

def get_audio_generator():
    """
    Get or create audio generator instance (singleton)
    """
    global _audio_generator
    if _audio_generator is None:
        _audio_generator = AudioGenerator()
    return _audio_generator