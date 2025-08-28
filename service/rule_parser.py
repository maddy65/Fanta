def load_rules(rules_path: str):
    rules = []
    with open(rules_path, "r") as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                rules.append(line.strip())
    return rules
