def load_rules(path):
    try:
        with open(path, "r") as f:
            lines = f.readlines()
        rules = [line.strip("- ").strip() for line in lines if line.startswith("- ")]
        return rules
    except FileNotFoundError:
        print("⚠️ Rules file not found.")
        return []
