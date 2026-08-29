"""
train.py
--------
Trains an NLP intent-classification model for the Student Support Chatbot.

Pipeline:
    1. Load labeled training examples from data/intents.json
    2. Preprocess text (lowercase, remove punctuation)
    3. Vectorize text using TF-IDF
    4. Train a Logistic Regression classifier over TF-IDF features
    5. Evaluate on a held-out test split
    6. Save the trained model + vectorizer to model/

Run:
    python train.py
"""

import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.pipeline import Pipeline

from preprocessing import clean_text

DATA_PATH = "data/intents.json"
MODEL_PATH = "model/intent_classifier.joblib"
INTENTS_META_PATH = "model/intents_meta.json"


def load_training_data(path: str):
    with open(path, "r") as f:
        data = json.load(f)

    texts, labels = [], []
    responses_by_tag = {}

    for intent in data["intents"]:
        tag = intent["tag"]
        responses_by_tag[tag] = intent["responses"]
        for example in intent["examples"]:
            texts.append(clean_text(example))
            labels.append(tag)

    return texts, labels, responses_by_tag


def train_and_evaluate():
    texts, labels, responses_by_tag = load_training_data(DATA_PATH)

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
        ("clf", LogisticRegression(max_iter=1000)),
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print(f"Test Accuracy: {acc:.2%}\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))
    print("Confusion Matrix (rows=true, cols=predicted):")
    labels_sorted = sorted(set(labels))
    cm = confusion_matrix(y_test, y_pred, labels=labels_sorted)
    print("Labels:", labels_sorted)
    print(cm)

    joblib.dump(pipeline, MODEL_PATH)
    with open(INTENTS_META_PATH, "w") as f:
        json.dump(responses_by_tag, f, indent=2)

    print(f"\nModel saved to {MODEL_PATH}")
    print(f"Intent responses saved to {INTENTS_META_PATH}")


if __name__ == "__main__":
    train_and_evaluate()
