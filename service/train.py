# service/train.py
import os
import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

MODEL_PATH = "model/model.pkl"

def generate_training_data(rules_texts):
    """
    Simple approach: rules_texts = list of strings (rules from MD files)
    Each rule will generate multiple positive/negative examples
    """
    X = []
    y = []

    for rule in rules_texts:
        # Positive example: snippet that violates the rule
        violation_snippet = f"VIOLATION: {rule}"  # placeholder, you can extract sample code
        X.append(violation_snippet)
        y.append(1)

        # Negative example: compliant snippet
        compliant_snippet = f"COMPLIANT: {rule}"  # placeholder
        X.append(compliant_snippet)
        y.append(0)

    return X, y

def train_model(rules_texts):
    print("🔧 Generating training data...")
    X_train, y_train = generate_training_data(rules_texts)

    print("📊 Vectorizing...")
    vectorizer = TfidfVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)

    print("🤖 Training model...")
    clf = LogisticRegression()
    clf.fit(X_train_vec, y_train)

    print("💾 Saving model...")
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump({"model": clf, "vectorizer": vectorizer}, MODEL_PATH)
    print(f"✅ Model saved at {MODEL_PATH}")

if __name__ == "__main__":
    from scanner.rule_loader import load_rules
    rules_texts = load_rules("rules")  # read all md files
    train_model(rules_texts)
