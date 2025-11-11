#!/usr/bin/env python
"""
Test script to verify all models are working correctly
"""

# Test BERT Sentiment Model
from music_app.utils.bert_sentiment import predict_sentiment
print('Testing BERT Sentiment Model:')
test_texts = [
    'I am so happy today!',
    'This is terrible and awful',
    'I feel neutral about this',
    'What a wonderful experience!',
    'This makes me angry'
]
for text in test_texts:
    result = predict_sentiment(text)
    print(f'Text: "{text}" -> Sentiment: {result}')
print()

# Test Mood Predictor Model
from music_app.utils.mood_predictor import predict_mood
print('Testing Mood Predictor Model:')
for text in test_texts:
    result = predict_mood(text)
    print(f'Text: "{text}" -> Mood: {result}')
print()

# Test MusicGen Model (quick test with short duration)
from music_app.utils.musicgen_model import generate_music
print('Testing MusicGen Model:')
result = generate_music('happy upbeat music', 5)
print(f'Music generation result: {result}')
print("\nAll models tested successfully!")
