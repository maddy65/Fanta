def generate_report(issues):
    return {
        "summary": {
            "total_issues": len(issues)
        },
        "issues": issues
    }
