# scanner/project_scanner.py
import os
import subprocess
from sklearn.exceptions import NotFittedError

def get_delta_files(project_path):
    """
    Use git to get changed files
    """
    cmd = ["git", "-C", project_path, "diff", "--name-only", "HEAD"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        files = [os.path.join(project_path, f.strip()) for f in result.stdout.splitlines()]
        print(f"[DEBUG] Delta files: {files}")
        return files
    except subprocess.CalledProcessError:
        return []

def extract_snippets(file_path):
    """
    Very basic: split file by lines or functions
    """
    snippets = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            snippets.append(content)
    except Exception as e:
        print(f"[ERROR] Could not read {file_path}: {e}")
    return snippets

def scan_project(project_path, rules, model=None, delta=False):
    results = []
    files_to_scan = get_delta_files(project_path) if delta else [os.path.join(project_path, f) for f in os.listdir(project_path) if f.endswith(".java")]

    for file_path in files_to_scan:
        snippets = extract_snippets(file_path)
        for snippet in snippets:
            violation = None
            if model:
                vectorizer = model["vectorizer"]
                clf = model["model"]
                try:
                    X_vec = vectorizer.transform([snippet])
                    pred = clf.predict(X_vec)[0]
                    violation = bool(pred)
                except NotFittedError:
                    violation = None
            results.append({
                "file": file_path,
                "snippet": snippet,
                "violation": violation
            })
    return results
