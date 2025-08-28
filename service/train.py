import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
from .rule_parser import load_rules

MODEL_PATH = "model.joblib"

def train_model(rules_path, training_data_path):
    rules = load_rules(rules_path)

    with open(training_data_path, "r") as f:
        training_data = json.load(f)

    texts = [item["code"] for item in training_data]
    labels = [item["label"] for item in training_data]

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(texts)

    clf = MultinomialNB()
    clf.fit(X, labels)

    joblib.dump((clf, vectorizer, rules), MODEL_PATH)
    print(f"✅ Model trained and saved at {MODEL_PATH}")
