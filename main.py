import argparse
import os
import json
import joblib

from scanner.rule_loader import load_rules
from scanner.project_scanner import scan_project
from scanner.report_generator import generate_report

MODEL_PATH = "model/model.pkl"


def main():
    parser = argparse.ArgumentParser(description="AI-powered Code Review Tool (MVP)")
    parser.add_argument("--project", required=True, help="Path to project source code")
    parser.add_argument("--output", default="reports/report.json", help="Path to save report")
    args = parser.parse_args()

    print("🔍 Loading rules...")
    rules = load_rules("rules/rules.md")

    model = None
    if os.path.exists(MODEL_PATH):
        print("🤖 Loading trained model...")
        model = joblib.load(MODEL_PATH)
    else:
        print("⚠️  No trained model found. Skipping AI checks.")

    print("📂 Scanning project:", args.project)
    scan_results = scan_project(args.project, rules, model)

    print("📝 Generating report...")
    report = generate_report(scan_results)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(report, f, indent=2)

    print(f"✅ Report saved at {args.output}")


if __name__ == "__main__":
    main()
