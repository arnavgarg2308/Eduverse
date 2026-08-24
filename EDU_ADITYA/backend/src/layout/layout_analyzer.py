import pymupdf


class LayoutAnalyzer:
    """
    Analyze the layout of a PDF using text block coordinates.
    """

    def analyze_pdf(self, pdf_path):
        """
        Analyze all pages of a PDF.

        Returns:
            list: Layout information for every page.
        """

        document = pymupdf.open(pdf_path)

        pages_data = []

        for page_number, page in enumerate(document):

            blocks = page.get_text("blocks")

            page_blocks = []

            for block in blocks:
                x0, y0, x1, y1, text, _, _ = block

                text = text.strip()

                if not text:
                    continue

                page_blocks.append({
                    "text": text,
                    "bounding_box": {
                        "x0": round(x0, 2),
                        "y0": round(y0, 2),
                        "x1": round(x1, 2),
                        "y1": round(y1, 2)
                    },
                    "width": round(x1 - x0, 2),
                    "height": round(y1 - y0, 2)
                })

            pages_data.append({
                "page_number": page_number + 1,
                "page_width": round(page.rect.width, 2),
                "page_height": round(page.rect.height, 2),
                "blocks": page_blocks
            })

        document.close()

        return pages_data
