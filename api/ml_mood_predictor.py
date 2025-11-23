"""
Machine Learning-based Mood Prediction and Sentiment Analysis
Uses pre-trained transformer models for accurate emotion detection
"""

import numpy as np
from transformers import pipeline
import torch

# Global model instances (loaded once)
_emotion_classifier = None
_sentiment_analyzer = None

def get_emotion_classifier():
    """
    Load emotion classification model (lazy loading)
    Using j-hartmann/emotion-english-distilroberta-base
    Detects: anger, disgust, fear, joy, neutral, sadness, surprise
    """
    global _emotion_classifier
    if _emotion_classifier is None:
        try:
            _emotion_classifier = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                top_k=None,
                device=0 if torch.cuda.is_available() else -1
            )
        except Exception as e:
            print(f"Error loading emotion classifier: {e}")
            _emotion_classifier = None
    return _emotion_classifier

def get_sentiment_analyzer():
    """
    Load sentiment analysis model (lazy loading)
    Using distilbert-base-uncased-finetuned-sst-2-english
    Detects: positive, negative
    """
    global _sentiment_analyzer
    if _sentiment_analyzer is None:
        try:
            _sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=0 if torch.cuda.is_available() else -1
            )
        except Exception as e:
            print(f"Error loading sentiment analyzer: {e}")
            _sentiment_analyzer = None
    return _sentiment_analyzer

# Emotion to mood mapping
EMOTION_TO_MOOD = {
    'joy': 'happy',
    'sadness': 'sad',
    'anger': 'angry',
    'fear': 'anxious',
    'surprise': 'excited',
    'disgust': 'angry',
    'neutral': 'calm'
}

# Enhanced mood mapping based on emotion combinations
MOOD_PROFILES = {
    'happy': ['joy', 'surprise'],
    'sad': ['sadness', 'fear'],
    'energetic': ['joy', 'surprise'],
    'calm': ['neutral'],
    'romantic': ['joy'],
    'angry': ['anger', 'disgust'],
    'anxious': ['fear', 'sadness'],
    'excited': ['surprise', 'joy'],
    'nostalgic': ['sadness', 'neutral']
}

def predict_mood_from_emotions(emotions):
    """
    Map detected emotions to music moods
    
    Args:
        emotions: List of emotion predictions with labels and scores
        
    Returns:
        tuple: (mood, confidence, emotion_scores)
    """
    if not emotions:
        return 'neutral', 0.5, {}
    
    # Get top emotion
    top_emotion = emotions[0]
    emotion_label = top_emotion['label'].lower()
    confidence = top_emotion['score']
    
    # Create emotion score dictionary
    emotion_scores = {e['label'].lower(): e['score'] for e in emotions}
    
    # Map emotion to mood
    mood = EMOTION_TO_MOOD.get(emotion_label, 'neutral')
    
    # Adjust mood based on emotion combinations
    if emotion_label == 'joy' and emotion_scores.get('surprise', 0) > 0.3:
        mood = 'energetic'
    elif emotion_label == 'sadness' and emotion_scores.get('neutral', 0) > 0.2:
        mood = 'nostalgic'
    elif emotion_label == 'joy' and confidence > 0.7:
        mood = 'happy'
    elif emotion_label == 'neutral' and emotion_scores.get('joy', 0) > 0.2:
        mood = 'calm'
    
    return mood, confidence, emotion_scores

def predict_mood_and_sentiment(text):
    """
    Advanced mood prediction using transformer models
    
    Args:
        text: Input text to analyze
        
    Returns:
        tuple: (mood, sentiment_score, confidence, emotions_dict)
    """
    if not text or not text.strip():
        return None, 0.0, 0.0, {}
    
    try:
        # Get emotion classifier
        emotion_classifier = get_emotion_classifier()
        sentiment_analyzer = get_sentiment_analyzer()
        
        if emotion_classifier is None or sentiment_analyzer is None:
            # Fallback to simple analysis
            return fallback_mood_prediction(text)
        
        # Predict emotions
        emotion_results = emotion_classifier(text[:512])[0]  # Limit text length
        
        # Predict sentiment
        sentiment_results = sentiment_analyzer(text[:512])[0]
        
        # Extract sentiment score (-1 to 1)
        sentiment_label = sentiment_results['label']
        sentiment_confidence = sentiment_results['score']
        sentiment_score = sentiment_confidence if sentiment_label == 'POSITIVE' else -sentiment_confidence
        
        # Get mood from emotions
        mood, confidence, emotion_scores = predict_mood_from_emotions(emotion_results)
        
        # Build comprehensive emotion dictionary
        emotions = {
            'primary_emotion': emotion_results[0]['label'].lower(),
            'emotion_scores': emotion_scores,
            'sentiment': sentiment_label.lower(),
            'sentiment_score': sentiment_score,
            'polarity': sentiment_score,
            'confidence': confidence,
            'intensity': confidence
        }
        
        return mood, sentiment_score, confidence, emotions
        
    except Exception as e:
        print(f"Error in ML mood prediction: {e}")
        return fallback_mood_prediction(text)

def fallback_mood_prediction(text):
    """
    Fallback mood prediction using keyword matching
    Used when ML models fail to load
    """
    from textblob import TextBlob
    
    MOOD_KEYWORDS = {
        'happy': ['happy', 'joy', 'excited', 'cheerful', 'delighted', 'wonderful', 'amazing', 'fantastic', 'great', 'awesome', 'love'],
        'sad': ['sad', 'depressed', 'down', 'unhappy', 'miserable', 'heartbroken', 'lonely', 'crying', 'hurt', 'pain'],
        'energetic': ['energetic', 'excited', 'pump', 'hype', 'fun', 'party', 'dance', 'active', 'motivated', 'intense'],
        'calm': ['calm', 'relax', 'peace', 'chill', 'soothing', 'tranquil', 'serene', 'quiet', 'gentle', 'peaceful'],
        'angry': ['angry', 'mad', 'furious', 'rage', 'annoyed', 'frustrated', 'irritated', 'hate', 'aggressive'],
        'romantic': ['love', 'romantic', 'romance', 'heart', 'crush', 'date', 'valentine', 'affection', 'tender'],
        'anxious': ['anxious', 'worried', 'nervous', 'stressed', 'tense', 'uneasy', 'concerned', 'fear', 'scared'],
        'nostalgic': ['nostalgic', 'memories', 'remember', 'past', 'old times', 'throwback', 'reminisce', 'miss']
    }
    
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    txt = text.lower()
    mood_scores = {}
    
    for mood, keywords in MOOD_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in txt)
        if score > 0:
            mood_scores[mood] = score
    
    if mood_scores:
        primary_mood = max(mood_scores, key=mood_scores.get)
        confidence = min(mood_scores[primary_mood] / 3.0, 1.0)
    else:
        if polarity > 0.5:
            primary_mood = "happy"
            confidence = min(polarity, 1.0)
        elif polarity < -0.4:
            primary_mood = "sad"
            confidence = min(abs(polarity), 1.0)
        else:
            primary_mood = "neutral"
            confidence = 0.5
    
    emotions = {
        'polarity': polarity,
        'confidence': confidence,
        'intensity': confidence,
        'method': 'fallback'
    }
    
    return primary_mood, polarity, confidence, emotions

def analyze_text_sentiment(text):
    """
    Comprehensive sentiment analysis with detailed metrics
    
    Args:
        text: Input text to analyze
        
    Returns:
        dict: Detailed analysis results
    """
    mood, sentiment_score, confidence, emotions = predict_mood_and_sentiment(text)
    
    # Generate sentiment label
    if sentiment_score > 0.5:
        sentiment_label = "Very Positive"
    elif sentiment_score > 0.1:
        sentiment_label = "Positive"
    elif sentiment_score < -0.5:
        sentiment_label = "Very Negative"
    elif sentiment_score < -0.1:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"
    
    # Calculate emotion intensity
    emotion_intensity = confidence
    
    return {
        'mood': mood,
        'sentiment_score': round(sentiment_score, 3),
        'sentiment_label': sentiment_label,
        'confidence': round(confidence, 3),
        'emotions': emotions,
        'text_length': len(text.split()),
        'emotion_intensity': round(emotion_intensity, 3),
        'model_used': 'transformer' if 'method' not in emotions else 'fallback'
    }

def batch_predict_moods(texts):
    """
    Predict moods for multiple texts efficiently
    
    Args:
        texts: List of text strings
        
    Returns:
        list: List of (mood, sentiment_score, confidence, emotions) tuples
    """
    results = []
    for text in texts:
        result = predict_mood_and_sentiment(text)
        results.append(result)
    return results

def get_mood_recommendations(mood, intensity=0.5):
    """
    Get music recommendations based on mood and intensity
    
    Args:
        mood: Detected mood
        intensity: Emotion intensity (0-1)
        
    Returns:
        dict: Recommended music parameters
    """
    recommendations = {
        'happy': {
            'genres': ['pop', 'dance', 'funk', 'disco'],
            'audio_features': {'valence': 0.7 + intensity * 0.2, 'energy': 0.6 + intensity * 0.3, 'danceability': 0.7}
        },
        'sad': {
            'genres': ['acoustic', 'indie', 'soul', 'blues'],
            'audio_features': {'valence': 0.2 - intensity * 0.1, 'energy': 0.3, 'acousticness': 0.6}
        },
        'energetic': {
            'genres': ['electronic', 'rock', 'hip-hop', 'edm'],
            'audio_features': {'energy': 0.8 + intensity * 0.2, 'danceability': 0.8, 'tempo': 130 + intensity * 20}
        },
        'calm': {
            'genres': ['ambient', 'classical', 'jazz', 'lofi'],
            'audio_features': {'valence': 0.5, 'energy': 0.2 + intensity * 0.1, 'acousticness': 0.7}
        },
        'romantic': {
            'genres': ['r&b', 'soul', 'pop', 'jazz'],
            'audio_features': {'valence': 0.6, 'energy': 0.4, 'acousticness': 0.5}
        },
        'angry': {
            'genres': ['metal', 'rock', 'punk', 'rap'],
            'audio_features': {'energy': 0.9, 'valence': 0.3, 'loudness': -5}
        },
        'anxious': {
            'genres': ['ambient', 'classical', 'meditation', 'lofi'],
            'audio_features': {'energy': 0.3, 'valence': 0.4, 'acousticness': 0.7}
        },
        'excited': {
            'genres': ['pop', 'electronic', 'dance', 'party'],
            'audio_features': {'energy': 0.85, 'valence': 0.8, 'danceability': 0.8}
        },
        'nostalgic': {
            'genres': ['classic rock', 'oldies', 'retro', 'indie'],
            'audio_features': {'valence': 0.5, 'acousticness': 0.6, 'energy': 0.4}
        }
    }
    
    return recommendations.get(mood, recommendations['calm'])
