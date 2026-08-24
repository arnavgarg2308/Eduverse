from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

output_path = "sample_data/input/sample.pdf"

doc = SimpleDocTemplate(output_path, pagesize=A4)
styles = getSampleStyleSheet()
story = []

# Title
story.append(Paragraph("Introduction to Artificial Intelligence", styles["Title"]))
story.append(Spacer(1, 20))

# Heading
story.append(Paragraph("1. What is Artificial Intelligence?", styles["Heading1"]))
story.append(Spacer(1, 10))

story.append(Paragraph(
    "Artificial Intelligence, commonly known as AI, is a branch of computer science "
    "that focuses on building systems capable of performing tasks that normally "
    "require human intelligence.",
    styles["BodyText"]
))
story.append(Spacer(1, 15))

story.append(Paragraph("2. Machine Learning", styles["Heading1"]))
story.append(Spacer(1, 10))

story.append(Paragraph(
    "Machine Learning is a subset of Artificial Intelligence. It enables computers "
    "to learn patterns from data and improve their performance without being "
    "explicitly programmed for every task.",
    styles["BodyText"]
))
story.append(Spacer(1, 15))

# Exercises
story.append(Paragraph("Exercises", styles["Heading1"]))
story.append(Spacer(1, 10))

story.append(Paragraph(
    "1. Define Artificial Intelligence in your own words.",
    styles["BodyText"]
))
story.append(Spacer(1, 8))

story.append(Paragraph(
    "2. What is the difference between Artificial Intelligence and Machine Learning?",
    styles["BodyText"]
))
story.append(Spacer(1, 8))

story.append(Paragraph(
    "3. Give three real-world applications of AI.",
    styles["BodyText"]
))

# Second page
story.append(PageBreak())

story.append(Paragraph("Deep Learning", styles["Title"]))
story.append(Spacer(1, 20))

story.append(Paragraph("3. Introduction to Deep Learning", styles["Heading1"]))
story.append(Spacer(1, 10))

story.append(Paragraph(
    "Deep Learning is a specialized area of Machine Learning that uses artificial "
    "neural networks with multiple layers to learn complex patterns from large datasets.",
    styles["BodyText"]
))
story.append(Spacer(1, 15))

story.append(Paragraph("Exercises", styles["Heading1"]))
story.append(Spacer(1, 10))

story.append(Paragraph(
    "1. What is Deep Learning?",
    styles["BodyText"]
))

doc.build(story)

print(f"Sample PDF created successfully: {output_path}")
