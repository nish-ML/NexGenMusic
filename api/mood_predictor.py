from textblob import TextBlob
import re

# Enhanced mood keywords for better sentiment analysis
MOOD_KEYWORDS = {
    'happy': ['happy', 'joy', 'excited', 'cheerful', 'delighted', 'pleased', 'glad', 'wonderful', 'amazing', 'fantastic', 'great', 'awesome', 'love', 'blessed', 'grateful'],
    'sad': ['sad', 'depressed', 'down', 'unhappy', 'miserable', 'heartbroken', 'lonely', 'crying', 'tears', 'hurt', 'pain', 'sorrow', 'grief', 'melancholy'],
    'energetic': ['energetic', 'excited', 'pump', 'hype', 'fun', 'party', 'dance', 'active', 'motivated', 'pumped', 'fired up', 'intense', 'powerful', 'strong'],
    'calm': ['calm', 'relax', 'peace', 'chill', 'soothing', 'tranquil', 'serene', 'quiet', 'gentle', 'soft', 'mellow', 'peaceful', 'meditate'],
    'angry': ['angry', 'mad', 'furious', 'rage', 'annoyed', 'frustrated', 'irritated', 'pissed', 'hate', 'aggressive'],
    'romantic': ['love', 'romantic', 'romance', 'heart', 'crush', 'date', 'valentine', 'affection', 'tender', 'sweet'],
    'anxious': ['anxious', 'worried', 'nervous', 'stressed', 'tense', 'uneasy', 'concerned', 'fear', 'scared', 'panic'],
    'nostalgic': ['nostalgic', 'memories', 'remember', 'past', 'old times', 'throwback', 'reminisce', 'miss']
}

def predict_mood_and_sentiment(text):
    """
    Enhanced mood prediction with sentiment analysis
    Returns (mood, sentiment_score, confidence, emotions)
    - mood: primary detected mood
    - sentiment_score: polarity (-1 to 1)
    - confidence: confidence score (0 to 1)
    - emotions: dict of detected emotions with scores
    """
    if not text or not text.strip():
        return None, 0.0, 0.0, {}
    
    # Sentiment analysis using TextBlob
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1.0 .. 1.0
    subjectivity = blob.sentiment.subjectivity  # 0.0 .. 1.0
    
    txt = text.lower()
    
    # Count mood keyword matches
    mood_scores = {}
    for mood, keywords in MOOD_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in txt)
        if score > 0:
            mood_scores[mood] = score
    
    # Determine primary mood based on keywords and polarity
    if mood_scores:
        # Get mood with highest keyword match
        primary_mood = max(mood_scores, key=mood_scores.get)
        confidence = min(mood_scores[primary_mood] / 3.0, 1.0)  # Normalize confidence
    else:
        # Fallback to polarity-based mood detection
        if polarity > 0.5:
            primary_mood = "happy"
            confidence = min(polarity, 1.0)
        elif polarity > 0.2:
            primary_mood = "calm"
            confidence = 0.6
        elif polarity < -0.4:
            primary_mood = "sad"
            confidence = min(abs(polarity), 1.0)
        elif polarity < -0.1:
            primary_mood = "anxious"
            confidence = 0.5
        else:
            primary_mood = "neutral"
            confidence = 0.4
    
    # Adjust confidence based on subjectivity
    confidence = confidence * (0.5 + subjectivity * 0.5)
    
    # Build emotion profile
    emotions = {
        'polarity': round(polarity, 3),
        'subjectivity': round(subjectivity, 3),
        'intensity': round(confidence, 3)
    }
    
    return primary_mood, polarity, confidence, emotions

def analyze_text_sentiment(text):
    """
    Comprehensive sentiment analysis
    Returns detailed analysis including mood, emotions, and recommendations
    """
    mood, polarity, confidence, emotions = predict_mood_and_sentiment(text)
    
    # Generate mood description
    if polarity > 0.5:
        sentiment_label = "Very Positive"
    elif polarity > 0.1:
        sentiment_label = "Positive"
    elif polarity < -0.5:
        sentiment_label = "Very Negative"
    elif polarity < -0.1:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"
    
    return {
        'mood': mood,
        'sentiment_score': polarity,
        'sentiment_label': sentiment_label,
        'confidence': confidence,
        'emotions': emotions,
        'text_length': len(text.split())
    }
