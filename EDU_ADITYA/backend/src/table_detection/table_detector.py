import pymupdf


class TableDetector:
    """
    Detect tables in a PDF using PyMuPDF.
    """

    def detect_tables(self, pdf_path):
        """
        Detect tables from all pages of a PDF.

        Returns:
            list: Detected tables grouped by page.
        """

        document = pymupdf.open(pdf_path)

        pages_data = []

        try:
            for page_number, page in enumerate(document):

                tables = page.find_tables()

                detected_tables = []

                for table_index, table in enumerate(tables.tables):

                    table_data = table.extract()

                    detected_tables.append({
                        "table_number": table_index + 1,
                        "data": table_data,
                        "bounding_box": {
                            "x0": round(table.bbox[0], 2),
                            "y0": round(table.bbox[1], 2),
                            "x1": round(table.bbox[2], 2),
                            "y1": round(table.bbox[3], 2)
                        }
                    })

                pages_data.append({
                    "page_number": page_number + 1,
                    "table_count": len(detected_tables),
                    "tables": detected_tables
                })

            return pages_data

        finally:
            document.close()
