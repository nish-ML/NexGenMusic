from transformers import pipeline

# Lazy loading of the emotion classification model
emotion_classifier = None

def predict_mood(text: str):
    """
    Predicts the top emotion for a given text using a fine-tuned RoBERTa model.
    Uses improved mapping and confidence thresholds for better accuracy.
    """
    global emotion_classifier
    if emotion_classifier is None:
        emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

    result = emotion_classifier(text)[0]
    top_emotion = max(result, key=lambda x: x["score"])

    # Get confidence score
    confidence = top_emotion["score"]

    # Improved emotion to mood mapping with better logic
    emotion_to_mood = {
        "joy": "happy",
        "anger": "angry",
        "sadness": "sad",
        "fear": "calm",
        "surprise": "happy",  # Changed from calm to happy
        "disgust": "angry",   # Changed from calm to angry
        "neutral": "calm"
    }

    # Special handling for low confidence predictions
    if confidence < 0.3:
        # For low confidence, check for explicit mood words
        text_lower = text.lower()
        if any(word in text_lower for word in ["happy", "joy", "excited", "great", "wonderful", "amazing"]):
            return "happy"
        elif any(word in text_lower for word in ["sad", "depressed", "unhappy", "terrible", "awful", "horrible"]):
            return "sad"
        elif any(word in text_lower for word in ["angry", "mad", "furious", "annoyed", "hate", "frustrated"]):
            return "angry"
        elif any(word in text_lower for word in ["calm", "peaceful", "relaxed", "neutral", "okay", "chill", "cool"]):
            return "calm"

    # For negative sentiment words, override neutral predictions
    text_lower = text.lower()
    if any(word in text_lower for word in ["terrible", "awful", "horrible", "bad", "worst"]) and top_emotion["label"] == "neutral":
        return "sad"

    return emotion_to_mood.get(top_emotion["label"], "calm")
