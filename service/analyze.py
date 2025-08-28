import os
import json
import joblib
from .rule_parser import load_rules

MODEL_PATH = "model.joblib"

def analyze_project(project_path, rules_path, report_path):
    if not os.path.exists(MODEL_PATH):
        print("⚠️ No trained model found. Run training first.")
        return

    clf, vectorizer, trained_rules = joblib.load(MODEL_PATH)
    rules = load_rules(rules_path)

    results = []

    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    code = f.read()

                X = vectorizer.transform([code])
                prediction = clf.predict(X)[0]

                violated_rules = [r for r in rules if r not in code]
                results.append({
                    "file": file_path,
                    "prediction": prediction,
                    "violated_rules": violated_rules
                })

    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"📄 Report generated at {report_path}")
