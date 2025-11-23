"""
MIDI-Based Music Generator
Integrates with mood detection to create MIDI melodies and convert to audio
"""

import os
import random
import subprocess
from midiutil import MIDIFile
from datetime import datetime
from .ml_mood_predictor import predict_mood_and_sentiment

class MIDIMusicGenerator:
    """
    Generate MIDI-based music from mood detection
    """
    
    def __init__(self):
        self.output_dir = "generated_music"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Note mappings
        self.NOTE_MAP = {
            "C3": 48, "D3": 50, "E3": 52, "F3": 53, "G3": 55, "A3": 57, "B3": 59,
            "C4": 60, "D4": 62, "E4": 64, "F4": 65, "G4": 67, "A4": 69, "B4": 71, 
            "C5": 72, "D5": 74, "E5": 76, "F5": 77, "G5": 79, "A5": 81, "B5": 83,
            "C6": 84
        }
        
        # Mood-based musical parameters
        self.mood_configs = {
            "happy": {
                "notes": ["C4", "E4", "G4", "A4", "C5", "E5"],
                "tempo": 140,
                "scale": "major",
                "instrument": 1,  # Piano
                "rhythm_pattern": [0.5, 0.25, 0.25, 0.5],
                "chord_progression": ["C4", "F4", "G4", "C4"]
            },
            "sad": {
                "notes": ["A3", "C4", "D4", "F4", "A4"],
                "tempo": 80,
                "scale": "minor",
                "instrument": 1,  # Piano
                "rhythm_pattern": [1.0, 0.5, 0.5, 1.0],
                "chord_progression": ["A3", "F4", "C4", "G4"]
            },
            "energetic": {
                "notes": ["E4", "G4", "B4", "D5", "E5", "G5"],
                "tempo": 160,
                "scale": "major",
                "instrument": 25,  # Electric Guitar
                "rhythm_pattern": [0.25, 0.25, 0.5, 0.25, 0.25],
                "chord_progression": ["E4", "A4", "B4", "E4"]
            },
            "calm": {
                "notes": ["D4", "E4", "G4", "A4", "D5"],
                "tempo": 100,
                "scale": "pentatonic",
                "instrument": 1,  # Piano
                "rhythm_pattern": [0.75, 0.5, 0.75, 1.0],
                "chord_progression": ["D4", "G4", "A4", "D4"]
            },
            "romantic": {
                "notes": ["G4", "B4", "D5", "F5", "G5"],
                "tempo": 90,
                "scale": "major",
                "instrument": 1,  # Piano
                "rhythm_pattern": [0.5, 0.5, 1.0, 0.5],
                "chord_progression": ["G4", "C5", "D5", "G4"]
            },
            "angry": {
                "notes": ["E3", "G3", "A3", "C4", "D4", "E4"],
                "tempo": 160,
                "scale": "minor",
                "instrument": 30,  # Distorted Guitar
                "rhythm_pattern": [0.25, 0.25, 0.25, 0.5],
                "chord_progression": ["E3", "A3", "B3", "E3"]
            },
            "anxious": {
                "notes": ["F4", "G4", "A4", "C5", "D5"],
                "tempo": 120,
                "scale": "minor",
                "instrument": 1,  # Piano
                "rhythm_pattern": [0.25, 0.5, 0.25, 0.5],
                "chord_progression": ["F4", "G4", "A4", "F4"]
            }
        }
    
    def generate_music_from_text(self, text, duration=40):
        """
        Generate music from text input using mood detection
        
        Args:
            text: Input text to analyze
            duration: Duration in seconds (default 40)
            
        Returns:
            dict: Generated music info with file paths
        """
        # Analyze mood from text
        mood, sentiment_score, confidence, emotions = predict_mood_and_sentiment(text)
        
        # Generate music based on detected mood
        return self.generate_music(mood, sentiment_score, confidence, duration)
    
    def generate_music(self, mood, sentiment_score=0.0, confidence=0.5, duration=40):
        """
        Generate MIDI music based on mood
        
        Args:
            mood: Detected mood
            sentiment_score: Sentiment polarity (-1 to 1)
            confidence: Confidence score (0 to 1)
            duration: Duration in seconds
            
        Returns:
            dict: Generated music info
        """
        # Get mood configuration
        config = self.mood_configs.get(mood.lower(), self.mood_configs["calm"])
        
        # Adjust parameters based on sentiment and confidence
        tempo = self._adjust_tempo(config["tempo"], sentiment_score, confidence)
        melody_length = max(20, int(duration * tempo / 60 / 2))  # Approximate notes for duration
        
        # Generate melody
        melody = self._generate_melody(config, melody_length, sentiment_score)
        
        # Create MIDI file
        midi_file = self._create_midi_file(melody, config, tempo, mood)
        
        # Convert to WAV (if possible)
        wav_file = self._convert_to_wav(midi_file)
        
        return {
            "mood": mood,
            "sentiment_score": sentiment_score,
            "confidence": confidence,
            "tempo": tempo,
            "melody_length": melody_length,
            "midi_file": midi_file,
            "wav_file": wav_file,
            "duration": duration,
            "notes_used": config["notes"],
            "instrument": config["instrument"]
        }
    
    def _adjust_tempo(self, base_tempo, sentiment_score, confidence):
        """
        Adjust tempo based on sentiment and confidence
        """
        # Positive sentiment increases tempo, negative decreases
        sentiment_adjustment = sentiment_score * 20
        
        # Higher confidence makes tempo more extreme
        confidence_multiplier = 1 + (confidence - 0.5) * 0.4
        
        adjusted_tempo = int((base_tempo + sentiment_adjustment) * confidence_multiplier)
        return max(60, min(200, adjusted_tempo))  # Keep within reasonable range
    
    def _generate_melody(self, config, length, sentiment_score):
        """
        Generate melody based on mood configuration
        """
        notes = config["notes"]
        rhythm_pattern = config["rhythm_pattern"]
        
        melody = []
        
        for i in range(length):
            # Choose note (with some randomness but mood-appropriate)
            if sentiment_score > 0.3:
                # Positive sentiment: prefer higher notes
                note = random.choice(notes[len(notes)//2:])
            elif sentiment_score < -0.3:
                # Negative sentiment: prefer lower notes
                note = random.choice(notes[:len(notes)//2 + 1])
            else:
                # Neutral: any note
                note = random.choice(notes)
            
            # Choose duration from rhythm pattern
            duration = random.choice(rhythm_pattern)
            
            melody.append({
                "note": note,
                "duration": duration,
                "velocity": random.randint(70, 100)
            })
        
        return melody
    
    def _create_midi_file(self, melody, config, tempo, mood):
        """
        Create MIDI file from melody
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{mood}_{tempo}bpm_{timestamp}.mid"
        filepath = os.path.join(self.output_dir, filename)
        
        # Create MIDI file
        midi = MIDIFile(1)
        track = 0
        
        midi.addTrackName(track, 0, f"{mood.title()} Melody")
        midi.addTempo(track, 0, tempo)
        midi.addProgramChange(track, 0, 0, config["instrument"])
        
        # Add melody notes
        time = 0
        for note_info in melody:
            note_name = note_info["note"]
            duration = note_info["duration"]
            velocity = note_info["velocity"]
            
            if note_name in self.NOTE_MAP:
                midi_note = self.NOTE_MAP[note_name]
                midi.addNote(track, 0, midi_note, time, duration, velocity)
            
            time += duration
        
        # Add simple chord progression as harmony
        self._add_harmony(midi, track, config, tempo, time)
        
        # Save MIDI file
        with open(filepath, "wb") as f:
            midi.writeFile(f)
        
        return filepath
    
    def _add_harmony(self, midi, track, config, tempo, melody_duration):
        """
        Add simple chord progression as harmony
        """
        chord_progression = config["chord_progression"]
        chord_duration = melody_duration / len(chord_progression)
        
        time = 0
        for chord_root in chord_progression:
            if chord_root in self.NOTE_MAP:
                root_note = self.NOTE_MAP[chord_root]
                
                # Add triad (root, third, fifth)
                midi.addNote(track, 1, root_note, time, chord_duration, 60)
                midi.addNote(track, 1, root_note + 4, time, chord_duration, 50)  # Third
                midi.addNote(track, 1, root_note + 7, time, chord_duration, 50)  # Fifth
            
            time += chord_duration
    
    def _convert_to_wav(self, midi_file):
        """
        Convert MIDI to WAV using FluidSynth (if available)
        """
        if not os.path.exists(midi_file):
            return None
        
        wav_file = midi_file.replace('.mid', '.wav')
        
        # Try to find FluidSynth and a soundfont
        soundfonts = [
            "/usr/share/sounds/sf2/FluidR3_GM.sf2",  # Linux
            "/System/Library/Components/CoreAudio.component/Contents/Resources/gs_instruments.dls",  # macOS
            "C:\\Windows\\System32\\drivers\\gm.dls",  # Windows
        ]
        
        fluidsynth_cmd = None
        soundfont = None
        
        # Check for FluidSynth
        try:
            subprocess.run(["fluidsynth", "--version"], capture_output=True, check=True)
            fluidsynth_cmd = "fluidsynth"
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                subprocess.run(["fluid-synth", "--version"], capture_output=True, check=True)
                fluidsynth_cmd = "fluid-synth"
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass
        
        # Find soundfont
        for sf in soundfonts:
            if os.path.exists(sf):
                soundfont = sf
                break
        
        # Convert if both FluidSynth and soundfont are available
        if fluidsynth_cmd and soundfont:
            try:
                cmd = [
                    fluidsynth_cmd, "-ni", soundfont, midi_file,
                    "-F", wav_file, "-r", "44100"
                ]
                subprocess.run(cmd, capture_output=True, check=True)
                
                if os.path.exists(wav_file):
                    return wav_file
            except subprocess.CalledProcessError:
                pass
        
        return None
    
    def get_music_info(self, filepath):
        """
        Get information about generated music file
        """
        if not os.path.exists(filepath):
            return None
        
        file_size = os.path.getsize(filepath)
        filename = os.path.basename(filepath)
        
        return {
            "filename": filename,
            "filepath": filepath,
            "size_kb": file_size / 1024,
            "format": "MIDI" if filepath.endswith('.mid') else "WAV"
        }

# Global instance
_midi_generator = None

def get_midi_generator():
    """
    Get or create MIDI generator instance (singleton)
    """
    global _midi_generator
    if _midi_generator is None:
        _midi_generator = MIDIMusicGenerator()
    return _midi_generator