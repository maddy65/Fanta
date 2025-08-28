def scan_project(project_path, rules, model=None, delta=False):
    if delta:
        print("⚡ Running in delta mode (only changed files)...")
        # Example: run git diff to get modified files
        import subprocess
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1"],
            cwd=project_path,
            capture_output=True,
            text=True
        )
        changed_files = result.stdout.strip().split("\n")
        # Filter only files you want to scan
        files_to_scan = [f for f in changed_files if f.endswith((".java", ".py", ".js"))]
    else:
        print("📂 Running in full project scan mode...")
        files_to_scan = []  # Collect all files from project_path

    # ✅ Continue with normal scan logic using files_to_scan
    scan_results = []
    for file in files_to_scan:
        # Your scanning logic here
        pass

    return scan_results
