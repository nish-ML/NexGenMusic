<<<<<<< HEAD
#!/usr/bin/env python
"""
Test script to evaluate sentiment and mood prediction accuracy using Kaggle datasets
"""

import kagglehub
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from music_app.utils.bert_sentiment import predict_sentiment
from music_app.utils.mood_predictor import predict_mood

def test_sentiment_accuracy():
    """Test sentiment analysis accuracy using IMDB dataset"""
    print("Testing Sentiment Analysis Accuracy...")

    # Download IMDB dataset
    path = kagglehub.dataset_download("lakshmi25npathi/imdb-dataset-of-50k-movie-reviews")
    df = pd.read_csv(f"{path}/IMDB Dataset.csv")

    # Sample 100 reviews for testing (50 positive, 50 negative)
    positive_reviews = df[df['sentiment'] == 'positive'].sample(50, random_state=42)
    negative_reviews = df[df['sentiment'] == 'negative'].sample(50, random_state=42)
    test_df = pd.concat([positive_reviews, negative_reviews])

    # Map ground truth
    sentiment_map = {'positive': 'POSITIVE', 'negative': 'NEGATIVE'}
    true_labels = [sentiment_map[s] for s in test_df['sentiment']]

    # Predict sentiments
    predicted_labels = []
    for review in test_df['review']:
        try:
            pred = predict_sentiment(review[:512])  # Limit text length
            predicted_labels.append(pred)
        except Exception as e:
            print(f"Error predicting sentiment: {e}")
            predicted_labels.append('POSITIVE')  # Default

    # Calculate accuracy
    accuracy = accuracy_score(true_labels, predicted_labels)
    print(".2f")
    print("\nClassification Report:")
    print(classification_report(true_labels, predicted_labels))

    return accuracy

def test_mood_accuracy():
    """Test mood prediction accuracy using emotion dataset"""
    print("\nTesting Mood Prediction Accuracy...")

    # Download emotion dataset
    path = kagglehub.dataset_download("parulpandey/emotion-dataset")
    df = pd.read_csv(f"{path}/validation.csv")

    # Sample 100 entries for testing
    test_df = df.sample(100, random_state=42)

    # Map emotions to moods (simplified mapping)
    emotion_to_mood = {
        'joy': 'happy',
        'anger': 'angry',
        'sadness': 'sad',
        'fear': 'calm',
        'surprise': 'happy',
        'love': 'happy',
        'neutral': 'calm'
    }

    true_labels = []
    for emotion in test_df['label']:
        mood = emotion_to_mood.get(emotion, 'calm')
        true_labels.append(mood)

    # Predict moods
    predicted_labels = []
    for text in test_df['text']:
        try:
            pred = predict_mood(text)
            predicted_labels.append(pred)
        except Exception as e:
            print(f"Error predicting mood: {e}")
            predicted_labels.append('calm')  # Default

    # Calculate accuracy
    accuracy = accuracy_score(true_labels, predicted_labels)
    print(".2f")
    print("\nClassification Report:")
    print(classification_report(true_labels, predicted_labels))

    return accuracy

if __name__ == "__main__":
    print("Evaluating Model Accuracy with Kaggle Datasets\n")

    sentiment_acc = test_sentiment_accuracy()
    mood_acc = test_mood_accuracy()

    print("\nSummary:")
    print(f"Sentiment Accuracy: {sentiment_acc:.2f}")
    print(f"Mood Accuracy: {mood_acc:.2f}")
=======
#!/usr/bin/env python
"""
Test script to evaluate sentiment and mood prediction accuracy using Kaggle datasets
"""

import kagglehub
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from music_app.utils.bert_sentiment import predict_sentiment
from music_app.utils.mood_predictor import predict_mood

def test_sentiment_accuracy():
    """Test sentiment analysis accuracy using IMDB dataset"""
    print("Testing Sentiment Analysis Accuracy...")

    # Download IMDB dataset
    path = kagglehub.dataset_download("lakshmi25npathi/imdb-dataset-of-50k-movie-reviews")
    df = pd.read_csv(f"{path}/IMDB Dataset.csv")

    # Sample 100 reviews for testing (50 positive, 50 negative)
    positive_reviews = df[df['sentiment'] == 'positive'].sample(50, random_state=42)
    negative_reviews = df[df['sentiment'] == 'negative'].sample(50, random_state=42)
    test_df = pd.concat([positive_reviews, negative_reviews])

    # Map ground truth
    sentiment_map = {'positive': 'POSITIVE', 'negative': 'NEGATIVE'}
    true_labels = [sentiment_map[s] for s in test_df['sentiment']]

    # Predict sentiments
    predicted_labels = []
    for review in test_df['review']:
        try:
            pred = predict_sentiment(review[:512])  # Limit text length
            predicted_labels.append(pred)
        except Exception as e:
            print(f"Error predicting sentiment: {e}")
            predicted_labels.append('POSITIVE')  # Default

    # Calculate accuracy
    accuracy = accuracy_score(true_labels, predicted_labels)
    print(".2f")
    print("\nClassification Report:")
    print(classification_report(true_labels, predicted_labels))

    return accuracy

def test_mood_accuracy():
    """Test mood prediction accuracy using emotion dataset"""
    print("\nTesting Mood Prediction Accuracy...")

    # Download emotion dataset
    path = kagglehub.dataset_download("parulpandey/emotion-dataset")
    df = pd.read_csv(f"{path}/validation.csv")

    # Sample 100 entries for testing
    test_df = df.sample(100, random_state=42)

    # Map emotions to moods (simplified mapping)
    emotion_to_mood = {
        'joy': 'happy',
        'anger': 'angry',
        'sadness': 'sad',
        'fear': 'calm',
        'surprise': 'happy',
        'love': 'happy',
        'neutral': 'calm'
    }

    true_labels = []
    for emotion in test_df['label']:
        mood = emotion_to_mood.get(emotion, 'calm')
        true_labels.append(mood)

    # Predict moods
    predicted_labels = []
    for text in test_df['text']:
        try:
            pred = predict_mood(text)
            predicted_labels.append(pred)
        except Exception as e:
            print(f"Error predicting mood: {e}")
            predicted_labels.append('calm')  # Default

    # Calculate accuracy
    accuracy = accuracy_score(true_labels, predicted_labels)
    print(".2f")
    print("\nClassification Report:")
    print(classification_report(true_labels, predicted_labels))

    return accuracy

if __name__ == "__main__":
    print("Evaluating Model Accuracy with Kaggle Datasets\n")

    sentiment_acc = test_sentiment_accuracy()
    mood_acc = test_mood_accuracy()

    print("\nSummary:")
    print(f"Sentiment Accuracy: {sentiment_acc:.2f}")
    print(f"Mood Accuracy: {mood_acc:.2f}")
>>>>>>> c25426a0d49250110b7f88b1d3e91981b8699196
