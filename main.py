import os
import subprocess
from pathlib import Path
import argparse

# Import rules
from rules.line_length_rule import LineLengthRule
from rules.naming_convention_rule import NamingConventionRule
from rules.comment_rule import CommentRule

# -------------------------------
# Utility to get git-changed files
# -------------------------------
def get_changed_files(project_path):
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True
        )
        changed = []
        for line in result.stdout.splitlines():
            status, file = line[:2], line[3:]
            # M = modified, A = added, AM = added+modified, etc.
            if file.endswith(".java") and status.strip() in {"M", "A", "AM"}:
                changed.append(os.path.join(project_path, file))
        return changed
    except Exception as e:
        print(f"[WARN] Could not get git changes: {e}")
        return []

# -------------------------------
# Main execution
# -------------------------------
def main():
    parser = argparse.ArgumentParser(description="Java Code Review Tool")
    parser.add_argument(
        "--project",
        default=constants.DEFAULT_PROJECT_PATH,
        help="Path to project source code"
    )
    parser.add_argument(
        "--delta",
        action="store_true",
        help="Run only on git-modified Java files"
    )

    args = parser.parse_args()
    project_path = args.project

    # Choose file set
    if args.delta:
        print("[INFO] Running in DELTA mode (only changed .java files)")
        java_files = get_changed_files(project_path)
    else:
        print("[INFO] Running on FULL project scan")
        java_files = list(Path(project_path).rglob("*.java"))

    if not java_files:
        print("[INFO] No Java files found to analyze.")
        return

    # Initialize rules
    rules = [
        LineLengthRule(max_length=120),
        NamingConventionRule(),
        CommentRule(min_comment_ratio=0.05)
    ]

    # Run checks
    for file_path in java_files:
        print(f"\nAnalyzing: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            for rule in rules:
                issues = rule.check(content)
                for issue in issues:
                    print(f"  [ISSUE] {issue}")

if __name__ == "__main__":
    main()
