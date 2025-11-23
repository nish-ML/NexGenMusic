#!/usr/bin/env python
"""
Test script to evaluate the fine-tuned sentiment model
"""

from music_app.utils.bert_sentiment import predict_sentiment

def test_fine_tuned_model():
    """Test the fine-tuned sentiment model with sample texts"""
    print("Testing Fine-Tuned Sentiment Model...")

    test_texts = [
        "I love this!",
        "This is amazing",
        "I feel great",
        "This sucks",
        "I hate it",
        "It's okay",
        "Neutral feeling",
        "What a wonderful day!",
        "This is terrible",
        "I'm so happy"
    ]

    for text in test_texts:
        result = predict_sentiment(text)
        print(f"'{text}' -> {result}")

if __name__ == "__main__":
    test_fine_tuned_model()
