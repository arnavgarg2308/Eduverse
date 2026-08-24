import os
import pymupdf

from src.ocr.ocr_engine import OCREngine


class PDFOCR:
    def __init__(self):
        """
        Initialize the PDF OCR pipeline.
        """

        self.ocr_engine = OCREngine()

    def convert_page_to_image(
        self,
        pdf_path,
        page_number,
        output_dir="sample_data/output"
    ):
        """
        Convert one PDF page into a PNG image.
        """

        os.makedirs(output_dir, exist_ok=True)

        document = pymupdf.open(pdf_path)

        page = document[page_number]

        zoom = 2

        matrix = pymupdf.Matrix(zoom, zoom)

        pixmap = page.get_pixmap(matrix=matrix)

        output_path = os.path.join(
            output_dir,
            f"page_{page_number + 1}.png"
        )

        pixmap.save(output_path)

        document.close()

        return output_path

    def extract_text_from_pdf(self, pdf_path):
        """
        Extract text from every PDF page using OCR.
        """

        document = pymupdf.open(pdf_path)

        page_count = len(document)

        document.close()

        all_pages_data = []

        for page_number in range(page_count):

            print(
                f"OCR processing page "
                f"{page_number + 1}/{page_count}"
            )

            image_path = self.convert_page_to_image(
                pdf_path,
                page_number
            )

            ocr_data = self.ocr_engine.extract_text_from_image(
                image_path
            )

            full_text = "\n".join(
                item["text"] for item in ocr_data
            )

            all_pages_data.append({
                "page_number": page_number + 1,
                "text": full_text,
                "ocr_blocks": ocr_data
            })

        return all_pages_data
