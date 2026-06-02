from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(
    filename,
    name,
    age,
    gender,
    phone,
    result,
    confidence
):

    pdf = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "SND Hospital",
            styles["Title"]
        )
    )

    content.append(
        Paragraph(
            "AI Lung Disease Detection Report",
            styles["Heading2"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            f"Patient Name: {name}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Age: {age}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Gender: {gender}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Phone: {phone}",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            f"Result: {result}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Confidence Score: {confidence}%",
            styles["Normal"]
        )
    )

    pdf.build(content)