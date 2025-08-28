import argparse
import os
import json
import joblib

from scanner.rule_loader import load_rules
from scanner.project_scanner import scan_project
from scanner.report_generator import generate_report
from constants import DEFAULT_PROJECT_PATH, DEFAULT_OUTPUT_PATH

MODEL_PATH = "model/model.pkl"

def main():
    parser = argparse.ArgumentParser(description="AI-powered Code Review Tool (MVP)")
    parser.add_argument(
        "--project",
        default=DEFAULT_PROJECT_PATH,
        help=f"Path to project source code (default: {DEFAULT_PROJECT_PATH})"
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT_PATH,
        help=f"Path to save report (default: {DEFAULT_OUTPUT_PATH})"
    )
    parser.add_argument(
        "--delta",
        action="store_true",
        help="Run only on git delta (changed files)"
    )
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
    scan_results = scan_project(args.project, rules, model, delta=args.delta)

    print("📝 Generating report...")
    report = generate_report(scan_results)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(report, f, indent=2)

    print(f"✅ Report saved at {args.output}")


if __name__ == "__main__":
    main()
