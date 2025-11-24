#!/usr/bin/env python
"""
Test script to verify audio generation is working
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexgenmusic.settings')
django.setup()

from api.audio_generator import get_audio_generator

def test_audio_generation():
    """Test basic audio generation"""
    print("Testing audio generation...")
    
    try:
        # Get audio generator
        generator = get_audio_generator()
        print("✓ Audio generator initialized")
        
        # Test generation
        print("\nGenerating test audio for 'happy' mood...")
        audio_file = generator.generate_mood_audio(
            mood='happy',
            sentiment_score=0.5,
            intensity=0.7
        )
        
        print(f"✓ Audio generated successfully: {audio_file}")
        
        # Check if file exists
        if os.path.exists(audio_file):
            file_size = os.path.getsize(audio_file)
            print(f"✓ File exists, size: {file_size:,} bytes")
            return True
        else:
            print("✗ File was not created")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_audio_generation()
    sys.exit(0 if success else 1)
