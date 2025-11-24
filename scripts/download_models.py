"""
Download and cache pre-trained models for mood prediction
Run this script once to download models before starting the server
"""

import os
os.environ['TRANSFORMERS_CACHE'] = './models_cache'

print("Downloading pre-trained models...")
print("This may take a few minutes on first run.\n")

try:
    from transformers import pipeline
    import torch
    
    device = 0 if torch.cuda.is_available() else -1
    device_name = "GPU" if device == 0 else "CPU"
    print(f"Using device: {device_name}\n")
    
    # Download emotion classification model
    print("1. Downloading emotion classification model...")
    print("   Model: j-hartmann/emotion-english-distilroberta-base")
    emotion_classifier = pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        top_k=None,
        device=device
    )
    print("   ✓ Emotion classifier downloaded successfully!\n")
    
    # Download sentiment analysis model
    print("2. Downloading sentiment analysis model...")
    print("   Model: distilbert-base-uncased-finetuned-sst-2-english")
    sentiment_analyzer = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        device=device
    )
    print("   ✓ Sentiment analyzer downloaded successfully!\n")
    
    # Test the models
    print("3. Testing models...")
    test_text = "I am feeling really happy and excited today!"
    
    print(f"   Test text: '{test_text}'")
    
    emotion_result = emotion_classifier(test_text)[0]
    print(f"   Emotion: {emotion_result[0]['label']} (confidence: {emotion_result[0]['score']:.2f})")
    
    sentiment_result = sentiment_analyzer(test_text)[0]
    print(f"   Sentiment: {sentiment_result['label']} (confidence: {sentiment_result['score']:.2f})")
    
    print("\n✓ All models downloaded and tested successfully!")
    print("\nYou can now start the Django server:")
    print("  python manage.py runserver")
    
except ImportError as e:
    print(f"\n✗ Error: Missing dependencies")
    print(f"  {e}")
    print("\nPlease install required packages:")
    print("  pip install transformers torch numpy scikit-learn")
    
except Exception as e:
    print(f"\n✗ Error downloading models: {e}")
    print("\nTroubleshooting:")
    print("  1. Check your internet connection")
    print("  2. Make sure you have enough disk space (~500MB)")
    print("  3. Try running again - downloads will resume if interrupted")
