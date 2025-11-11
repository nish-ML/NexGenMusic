<<<<<<< HEAD
from music_app.utils.bert_sentiment import predict_sentiment

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

expected = [
    "POSITIVE",
    "POSITIVE",
    "POSITIVE",
    "NEGATIVE",
    "NEGATIVE",
    "NEGATIVE",
    "POSITIVE",
    "NEUTRAL",
    "NEUTRAL",
    "POSITIVE"
]

correct = 0
print("Testing Fine-tuned Sentiment Model:")
print("=" * 50)

for i, text in enumerate(test_texts):
    pred = predict_sentiment(text)
    exp = expected[i]
    status = "✓" if pred == exp else "✗"
    print(f"{status} '{text}' -> {pred} (expected: {exp})")
    if pred == exp:
        correct += 1

accuracy = correct / len(test_texts) * 100
print(f"\nAccuracy: {correct}/{len(test_texts)} = {accuracy:.1f}%")

if accuracy == 100.0:
    print("🎉 Perfect! 100% accuracy achieved!")
else:
    print(f"Current accuracy: {accuracy:.1f}% - Room for improvement")
=======
from music_app.utils.bert_sentiment import predict_sentiment

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

expected = [
    "POSITIVE",
    "POSITIVE",
    "POSITIVE",
    "NEGATIVE",
    "NEGATIVE",
    "NEGATIVE",
    "POSITIVE",
    "NEUTRAL",
    "NEUTRAL",
    "POSITIVE"
]

correct = 0
print("Testing Fine-tuned Sentiment Model:")
print("=" * 50)

for i, text in enumerate(test_texts):
    pred = predict_sentiment(text)
    exp = expected[i]
    status = "✓" if pred == exp else "✗"
    print(f"{status} '{text}' -> {pred} (expected: {exp})")
    if pred == exp:
        correct += 1

accuracy = correct / len(test_texts) * 100
print(f"\nAccuracy: {correct}/{len(test_texts)} = {accuracy:.1f}%")

if accuracy == 100.0:
    print("🎉 Perfect! 100% accuracy achieved!")
else:
    print(f"Current accuracy: {accuracy:.1f}% - Room for improvement")
>>>>>>> c25426a0d49250110b7f88b1d3e91981b8699196
