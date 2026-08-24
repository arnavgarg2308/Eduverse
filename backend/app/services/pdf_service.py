from pypdf import PdfReader
from io import BytesIO


def extract_text_from_pdf(file_data: bytes):

    try:
        pdf_file = BytesIO(file_data)

        reader = PdfReader(pdf_file)

        extracted_text = ""

        for page in reader.pages:
            text = page.extract_text()

            if text:
                extracted_text += text + "\n"

        return extracted_text.strip()

    except Exception as e:
        raise Exception(
            f"Failed to extract text from PDF: {str(e)}"
        )