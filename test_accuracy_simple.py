#!/usr/bin/env python
"""
Simple test script to evaluate sentiment and mood prediction accuracy using sample data
"""

from music_app.utils.bert_sentiment import predict_sentiment
from music_app.utils.mood_predictor import predict_mood
from sklearn.metrics import accuracy_score, classification_report

def test_sentiment_simple():
    """Test sentiment analysis with sample data"""
    print("Testing Sentiment Analysis...")

    # Sample test data
    test_texts = [
        "I love this movie, it's amazing!",
        "This is the best day ever",
        "I feel so happy today",
        "This product is terrible",
        "I hate waiting in long lines",
        "This is awful and disappointing",
        "I'm quite chill and relaxed",
        "This is okay, nothing special",
        "I'm feeling neutral about this",
        "What a wonderful experience!"
    ]

    # Ground truth labels (POSITIVE/NEGATIVE/NEUTRAL)
    true_labels = [
        "POSITIVE", "POSITIVE", "POSITIVE",
        "NEGATIVE", "NEGATIVE", "NEGATIVE",
        "POSITIVE", "NEUTRAL", "NEUTRAL", "POSITIVE"
    ]

    predicted_labels = []
    for text in test_texts:
        pred = predict_sentiment(text)
        predicted_labels.append(pred)
        print(f"'{text}' -> {pred}")

    accuracy = accuracy_score(true_labels, predicted_labels)
    print(f"Sentiment Accuracy: {accuracy:.2f}")
    print("\nClassification Report:")
    print(classification_report(true_labels, predicted_labels))

    return accuracy

def test_mood_simple():
    """Test mood prediction with sample data"""
    print("\nTesting Mood Prediction...")

    # Sample test data
    test_texts = [
        "I love this movie, it's amazing!",
        "This is the best day ever",
        "I feel so happy today",
        "This product is terrible",
        "I hate waiting in long lines",
        "This is awful and disappointing",
        "I'm quite chill and relaxed",
        "This is okay, nothing special",
        "I'm feeling neutral about this",
        "What a wonderful experience!"
    ]

    # Ground truth moods
    true_labels = [
        "happy", "happy", "happy",
        "angry", "angry", "sad",
        "calm", "calm", "calm", "happy"
    ]

    predicted_labels = []
    for text in test_texts:
        pred = predict_mood(text)
        predicted_labels.append(pred)
        print(f"'{text}' -> {pred}")

    accuracy = accuracy_score(true_labels, predicted_labels)
    print(f"Mood Accuracy: {accuracy:.2f}")
    print("\nClassification Report:")
    print(classification_report(true_labels, predicted_labels))

    return accuracy

if __name__ == "__main__":
    print("Evaluating Model Accuracy with Sample Data\n")

    sentiment_acc = test_sentiment_simple()
    mood_acc = test_mood_simple()

    print("\nSummary:")
    print(f"Sentiment Accuracy: {sentiment_acc:.2f}")
    print(f"Mood Accuracy: {mood_acc:.2f}")
