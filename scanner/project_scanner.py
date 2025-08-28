import os

def scan_project(project_path, rules, model=None):
    issues = []
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                for rule in rules:
                    if "print()" in content and "print()" in rule:
                        issues.append({
                            "file": filepath,
                            "issue": "Avoid using print()",
                            "severity": "low"
                        })
                # (future: apply ML model here)
    return issues
