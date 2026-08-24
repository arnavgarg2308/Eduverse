import os
import unittest

from src.pipeline.document_analyzer import DocumentAnalyzer


class TestDocumentAnalyzer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.pdf_path = "sample_data/input/sample.pdf"

        cls.output_path = (
            "sample_data/output/"
            "test_full_document_analysis.json"
        )

        cls.analyzer = DocumentAnalyzer()

        # Remove old test output file before tests start
        if os.path.exists(cls.output_path):
            os.remove(cls.output_path)

        # Analyze without creating an output file
        cls.result = cls.analyzer.analyze(
            cls.pdf_path
        )

    @classmethod
    def tearDownClass(cls):

        # Remove generated test output file after tests finish
        if os.path.exists(cls.output_path):
            os.remove(cls.output_path)

    def test_analyzer_exists(self):

        self.assertIsNotNone(
            self.analyzer
        )

    def test_result_exists(self):

        self.assertIsNotNone(
            self.result
        )

    def test_result_is_dictionary(self):

        self.assertIsInstance(
            self.result,
            dict
        )

    def test_required_top_level_keys_exist(self):

        self.assertIn(
            "file_name",
            self.result
        )

        self.assertIn(
            "page_count",
            self.result
        )

        self.assertIn(
            "pages",
            self.result
        )

    def test_file_name(self):

        self.assertEqual(
            self.result["file_name"],
            "sample.pdf"
        )

    def test_page_count(self):

        self.assertEqual(
            self.result["page_count"],
            2
        )

    def test_pages_exist(self):

        self.assertIsInstance(
            self.result["pages"],
            list
        )

        self.assertGreater(
            len(self.result["pages"]),
            0
        )

    def test_page_count_matches_pages(self):

        self.assertEqual(
            len(self.result["pages"]),
            self.result["page_count"]
        )

    def test_page_structure(self):

        for page in self.result["pages"]:

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
            self.result["pages"],
            start=1
        ):

            self.assertEqual(
                page["page_number"],
                index
            )

    def test_page_text_exists(self):

        for page in self.result["pages"]:

            self.assertIsInstance(
                page["text"],
                str
            )

            self.assertGreater(
                len(page["text"].strip()),
                0
            )

    def test_analysis_without_output_file(self):

        # Ensure the output file does not exist before analysis
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

        result = self.analyzer.analyze(
            self.pdf_path
        )

        # Analysis should still return a valid result
        self.assertIsInstance(
            result,
            dict
        )

        # No JSON file should be created when no output path is provided
        self.assertFalse(
            os.path.exists(self.output_path)
        )

    def test_analysis_creates_json_output(self):

        # Remove old file before this specific test
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

        result = self.analyzer.analyze(
            self.pdf_path,
            self.output_path
        )

        self.assertTrue(
            os.path.exists(
                self.output_path
            )
        )

        self.assertEqual(
            result["file_name"],
            "sample.pdf"
        )

        self.assertEqual(
            result["page_count"],
            2
        )


if __name__ == "__main__":
    unittest.main()
