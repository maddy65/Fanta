import os

def load_rules(rules_dir="rules"):
    rules = []

    if os.path.isdir(rules_dir):
        for file in os.listdir(rules_dir):
            if file.endswith(".md"):
                file_path = os.path.join(rules_dir, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    rules.append(f.read())
        if rules:
            print(f"[DEBUG] Loaded {len(rules)} rule files from {rules_dir}")
        else:
            print(f"[DEBUG] No .md rule files found in {rules_dir}.")
    else:
        print(f"[DEBUG] Rules folder '{rules_dir}' not found.")

    return rules
