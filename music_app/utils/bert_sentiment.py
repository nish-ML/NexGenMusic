from transformers import pipeline

# Load fine-tuned sentiment model
sentiment_classifier = pipeline("sentiment-analysis", model="./sentiment_model")

def predict_sentiment(text: str):
    """
    Predicts sentiment (POSITIVE/NEGATIVE/NEUTRAL) for a given text.
    Includes custom logic for slang terms.
    """
    # Custom override for positive slang terms
    text_lower = text.lower()
    positive_words = ["chill", "cool", "awesome", "great", "fantastic", "amazing", "wonderful", "excellent"]
    if any(word in text_lower for word in positive_words):
        return "POSITIVE"

    # Custom override for neutral terms
    neutral_words = ["okay", "alright", "fine", "neutral", "nothing special", "average", "meh"]
    if any(word in text_lower for word in neutral_words):
        return "NEUTRAL"

    result = sentiment_classifier(text)[0]
    label = result["label"].lower()

    # Direct mapping for cardiffnlp model
    if label == "positive":
        return "POSITIVE"
    elif label == "negative":
        return "NEGATIVE"
    elif label == "neutral":
        return "NEUTRAL"
    else:
        return "NEUTRAL"  # Default fallback
