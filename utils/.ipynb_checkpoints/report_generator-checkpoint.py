from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.pagesizes import letter


def generate_report(
    filename,
    patient_summary
):

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    content = []

    title = Paragraph(
        "ICU AI Clinical Report",
        styles['Title']
    )

    content.append(title)

    content.append(
        Spacer(1, 20)
    )

    for item in patient_summary:

        para = Paragraph(
            item,
            styles['BodyText']
        )

        content.append(para)

        content.append(
            Spacer(1, 12)
        )

    doc.build(content)