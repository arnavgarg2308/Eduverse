from pathlib import Path
import pymupdf


class PDFReader:
    """
    Reads a PDF and extracts basic document information.
    """

    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)

        if not self.pdf_path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {self.pdf_path}"
            )

    def get_document_info(self) -> dict:
        """
        Extract basic information from the PDF.
        """

        document = pymupdf.open(self.pdf_path)

        try:
            metadata = document.metadata

            pages = []

            for page_number, page in enumerate(document):
                page_data = {
                    "page_number": page_number + 1,
                    "width": page.rect.width,
                    "height": page.rect.height,
                    "text": page.get_text(),
                }

                pages.append(page_data)

            return {
                "file_name": self.pdf_path.name,
                "page_count": len(document),
                "metadata": metadata,
                "pages": pages,
            }

        finally:
            document.close()
