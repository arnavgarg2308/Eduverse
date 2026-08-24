import unittest

from src.pdf_reader.reader import PDFReader


class TestPDFReader(unittest.TestCase):

    def setUp(self):

        self.pdf_path = "sample_data/input/sample.pdf"

        self.reader = PDFReader(self.pdf_path)

        self.document_info = (
            self.reader.get_document_info()
        )

    def test_file_name(self):

        self.assertEqual(
            self.document_info["file_name"],
            "sample.pdf"
        )

    def test_page_count(self):

        self.assertEqual(
            self.document_info["page_count"],
            2
        )

    def test_pages_exist(self):

        pages = self.document_info["pages"]

        self.assertEqual(
            len(pages),
            2
        )

    def test_page_numbers(self):

        pages = self.document_info["pages"]

        self.assertEqual(
            pages[0]["page_number"],
            1
        )

        self.assertEqual(
            pages[1]["page_number"],
            2
        )

    def test_page_text_exists(self):

        pages = self.document_info["pages"]

        self.assertTrue(
            len(pages[0]["text"]) > 0
        )

        self.assertTrue(
            len(pages[1]["text"]) > 0
        )

    def test_page_dimensions(self):

        pages = self.document_info["pages"]

        for page in pages:

            self.assertGreater(
                page["width"],
                0
            )

            self.assertGreater(
                page["height"],
                0
            )


if __name__ == "__main__":

    unittest.main()
