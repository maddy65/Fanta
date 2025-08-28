=import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def json_to_pdf(json_file, pdf_file):
    with open(json_file, "r") as f:
        data = json.load(f)

    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Code Review Report", styles["Title"]))
    elements.append(Spacer(1, 20))

    for issue in data.get("issues", []):
        rule = issue.get("rule", "Unknown Rule")
        line = issue.get("line", "N/A")
        suggestion = issue.get("suggestion", "No suggestion provided.")

        elements.append(Paragraph(f"Rule: {rule}", styles["Heading2"]))
        elements.append(Paragraph(f"Line: {line}", styles["Normal"]))
        elements.append(Paragraph(f"Suggestion: {suggestion}", styles["Normal"]))
        elements.append(Spacer(1, 10))

    doc.build(elements)
    print(f"PDF generated: {pdf_file}")


if __name__ == "__main__":
    json_to_pdf("reports/report.json", "output/report.pdf")
