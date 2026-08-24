import unittest

from src.pdf_reader.reader import PDFReader
from src.layout.layout_analyzer import LayoutAnalyzer
from src.heading_detection.heading_detector import HeadingDetector
from src.topic_detection.topic_detector import TopicDetector
from src.table_detection.table_detector import TableDetector
from src.document_structure.structure_builder import DocumentStructureBuilder


class TestDocumentStructureBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.pdf_path = "sample_data/input/sample.pdf"

        # Read PDF
        pdf_reader = PDFReader(cls.pdf_path)

        cls.document_info = pdf_reader.get_document_info()

        # Analyze layout
        layout_analyzer = LayoutAnalyzer()

        cls.layout_data = layout_analyzer.analyze_pdf(
            cls.pdf_path
        )

        # Detect headings
        heading_detector = HeadingDetector()

        cls.heading_data = heading_detector.detect_headings(
            cls.layout_data
        )

        # Detect topics
        topic_detector = TopicDetector()

        cls.topic_data = topic_detector.detect_topics(
            cls.document_info["pages"]
        )

        # Detect tables
        table_detector = TableDetector()

        cls.table_data = table_detector.detect_tables(
            cls.pdf_path
        )

        # Build document structure
        structure_builder = DocumentStructureBuilder()

        cls.document_structure = (
            structure_builder.build_structure(
                cls.document_info,
                cls.heading_data,
                cls.topic_data,
                cls.table_data
            )
        )

    def test_document_structure_exists(self):

        self.assertIsNotNone(
            self.document_structure
        )

    def test_document_structure_is_dictionary(self):

        self.assertIsInstance(
            self.document_structure,
            dict
        )

    def test_required_top_level_keys_exist(self):

        self.assertIn(
            "file_name",
            self.document_structure
        )

        self.assertIn(
            "page_count",
            self.document_structure
        )

        self.assertIn(
            "pages",
            self.document_structure
        )

    def test_file_name(self):

        self.assertEqual(
            self.document_structure["file_name"],
            "sample.pdf"
        )

    def test_page_count(self):

        self.assertEqual(
            self.document_structure["page_count"],
            2
        )

    def test_pages_exist(self):

        pages = self.document_structure["pages"]

        self.assertIsInstance(
            pages,
            list
        )

        self.assertGreater(
            len(pages),
            0
        )

    def test_page_count_matches_pages(self):

        self.assertEqual(
            len(self.document_structure["pages"]),
            self.document_structure["page_count"]
        )

    def test_page_structure(self):

        for page in self.document_structure["pages"]:

            self.assertIn(
                "page_number",
                page
            )

            self.assertIn(
                "text",
                page
            )

            self.assertIn(
                "headings",
                page
            )

            self.assertIn(
                "topics",
                page
            )

            self.assertIn(
                "tables",
                page
            )

    def test_page_numbers(self):

        for index, page in enumerate(
            self.document_structure["pages"],
            start=1
        ):

            self.assertEqual(
                page["page_number"],
                index
            )

    def test_page_text_exists(self):

        for page in self.document_structure["pages"]:

            self.assertIsInstance(
                page["text"],
                str
            )

            self.assertGreater(
                len(page["text"].strip()),
                0
            )

    def test_headings_is_list(self):

        for page in self.document_structure["pages"]:

            self.assertIsInstance(
                page["headings"],
                list
            )

    def test_topics_is_list(self):

        for page in self.document_structure["pages"]:

            self.assertIsInstance(
                page["topics"],
                list
            )

    def test_tables_is_list(self):

        for page in self.document_structure["pages"]:

            self.assertIsInstance(
                page["tables"],
                list
            )


if __name__ == "__main__":

    unittest.main()
