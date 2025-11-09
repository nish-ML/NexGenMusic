# enhanced_train_model.py
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
import joblib
import warnings
import os
import json


warnings.filterwarnings('ignore')

class MoodDataset(Dataset):
    def __init__(self, texts, labels, vectorizer):
        self.texts = texts
        self.labels = labels
        self.vectorizer = vectorizer

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]
        features = self.vectorizer.transform([text]).toarray().flatten()
        features = torch.tensor(features, dtype=torch.float32)
        return {
            'features': features,
            'labels': torch.tensor(label, dtype=torch.long)
        }

class EnhancedMoodClassifier(nn.Module):
    def __init__(self, input_size, n_classes, hidden_size=512):
        super(EnhancedMoodClassifier, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.bn1 = nn.BatchNorm1d(hidden_size)
        self.dropout1 = nn.Dropout(0.3)
        self.fc2 = nn.Linear(hidden_size, hidden_size // 2)
        self.bn2 = nn.BatchNorm1d(hidden_size // 2)
        self.dropout2 = nn.Dropout(0.3)
        self.fc3 = nn.Linear(hidden_size // 2, n_classes)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.bn1(self.fc1(x)))
        x = self.dropout1(x)
        x = self.relu(self.bn2(self.fc2(x)))
        x = self.dropout2(x)
        x = self.fc3(x)
        return x

def train_enhanced_mood_model(csv_file_path='emotion_dataset.csv', n_epochs=15, save_dir='.'):
    print("🎵 Training Enhanced Mood Detection Model...")
    print(f"Loading dataset from {csv_file_path}...")
    
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        print(f"❌ Error: File {csv_file_path} not found!")
        return None

    if 'text' not in df.columns or 'emotion' not in df.columns:
        raise ValueError("CSV must contain 'text' and 'emotion' columns")

    texts = df['text'].astype(str).values
    emotions = df['emotion'].astype(str).values

    print(f"✅ Dataset loaded: {len(texts)} samples")
    print("📊 Emotions distribution:")
    print(df['emotion'].value_counts())

    # Encode labels
    label_encoder = LabelEncoder()
    labels = label_encoder.fit_transform(emotions)

    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        max_features=5000,
        stop_words='english',
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.9
    )

    print("🔧 Fitting TF-IDF vectorizer...")
    X_tfidf = vectorizer.fit_transform(texts)
    print(f"✅ Vocabulary size: {len(vectorizer.get_feature_names_out())}")

    # Split data
    X_train, X_val, y_train, y_val = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )

    train_dataset = MoodDataset(X_train, y_train, vectorizer)
    val_dataset = MoodDataset(X_val, y_val, vectorizer)

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=32)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"🖥️ Using device: {device}")

    input_size = len(vectorizer.get_feature_names_out())
    model = EnhancedMoodClassifier(input_size=input_size, n_classes=len(label_encoder.classes_))
    model = model.to(device)

    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001, weight_decay=1e-4)
    criterion = nn.CrossEntropyLoss()

    best_accuracy = 0.0
    print("🚀 Starting training...")

    for epoch in range(n_epochs):
        model.train()
        total_loss = 0.0

        for batch in train_loader:
            optimizer.zero_grad()
            features = batch['features'].to(device)
            labels_batch = batch['labels'].to(device)
            outputs = model(features)
            loss = criterion(outputs, labels_batch)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            total_loss += loss.item()

        # Validation
        model.eval()
        val_predictions = []
        val_true = []

        with torch.no_grad():
            for batch in val_loader:
                features = batch['features'].to(device)
                labels_batch = batch['labels'].to(device)
                outputs = model(features)
                _, preds = torch.max(outputs, 1)
                val_predictions.extend(preds.cpu().numpy())
                val_true.extend(labels_batch.cpu().numpy())

        accuracy = accuracy_score(val_true, val_predictions)
        avg_loss = total_loss / len(train_loader)

        print(f"📈 Epoch {epoch+1}/{n_epochs} - Loss: {avg_loss:.4f} - Val Accuracy: {accuracy:.4f}")

        # Save best model
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            # Save model files
            torch.save(model.state_dict(), os.path.join(save_dir, 'enhanced_mood_model.pth'))
            joblib.dump(label_encoder, os.path.join(save_dir, 'label_encoder.pkl'))
            joblib.dump(vectorizer, os.path.join(save_dir, 'tfidf_vectorizer.pkl'))
            
            training_info = {
                'best_accuracy': best_accuracy,
                'n_epochs': n_epochs,
                'dataset_size': len(texts),
                'classes': list(label_encoder.classes_),
                'vocabulary_size': input_size
            }
            
            with open(os.path.join(save_dir, 'training_info.json'), 'w') as f:
                json.dump(training_info, f, indent=2)
                
            print(f"💾 New best model saved (accuracy={accuracy:.4f})")

    print("\n✅ Training complete!")
    print(f"🎯 Best accuracy: {best_accuracy:.4f}")
    print(f"😊 Detected emotions: {list(label_encoder.classes_)}")
    
    # Test the model
    print("\n🧪 Testing model with sample inputs...")
    test_texts = [
        "I am so happy today!",
        "I feel sad and lonely",
        "This makes me angry",
        "I'm scared of what might happen",
        "It's a normal day"
    ]
    
    # Simple prediction test
    model.eval()
    for text in test_texts:
        try:
            features = vectorizer.transform([text]).toarray().flatten()
            features_tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
            with torch.no_grad():
                outputs = model(features_tensor.to(device))
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                predicted_class = torch.argmax(outputs, dim=1)
                predicted_mood = label_encoder.inverse_transform(predicted_class.cpu().numpy())[0]
                confidence = probabilities[0][predicted_class].item()
                print(f"   '{text}' -> {predicted_mood} ({confidence:.2%})")
        except:
            pass
    
    return label_encoder.classes_

if __name__ == "__main__":
    try:
        print("=" * 60)
        print("🎵 AI MUSIC GENERATOR - MODEL TRAINING")
        print("=" * 60)
        
        classes = train_enhanced_mood_model(
            csv_file_path='emotion_dataset.csv', 
            n_epochs=15, 
            save_dir='.'
        )
        
        if classes is not None:
            print(f"\n🎉 Training completed successfully!")
            print(f"📁 Model files saved:")
            print(f"   - enhanced_mood_model.pth")
            print(f"   - label_encoder.pkl") 
            print(f"   - tfidf_vectorizer.pkl")
            print(f"   - training_info.json")
            print(f"\n🚀 Now run: streamlit run app.py")
        else:
            print("❌ Training failed!")
            
    except Exception as e:
        print(f"❌ Error during training: {str(e)}")
        print("\n💡 Make sure 'emotion_dataset.csv' exists in the current directory")