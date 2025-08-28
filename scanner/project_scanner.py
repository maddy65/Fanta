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
    Extract snippets intelligently:
    - If git diff available, capture only changed lines
    - Else fallback to function-level or line-level splits
    """
    snippets = []
    try:
        # Try git diff to get changed lines
        cmd = ["git", "-C", os.path.dirname(file_path), "diff", "-U0", "HEAD", "--", file_path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        diff_output = result.stdout.splitlines()
        for line in diff_output:
            if line.startswith("+") and not line.startswith("+++"):  # new code line
                snippets.append(line[1:].strip())

        # Fallback: if no diff found, return function-level blocks
        if not snippets:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                block = []
                for line in lines:
                    block.append(line.rstrip())
                    if line.strip().endswith("}"):  # end of function/class
                        snippets.append("\n".join(block))
                        block = []
                if block:  # leftover
                    snippets.append("\n".join(block))

    except Exception as e:
        print(f"[ERROR] Could not read {file_path}: {e}")
    return snippets

def scan_project(project_path, rules, model=None, delta=False):
    results = []
    files_to_scan = get_delta_files(project_path) if delta else [
        os.path.join(project_path, f) for f in os.listdir(project_path) if f.endswith(".java")
    ]

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
