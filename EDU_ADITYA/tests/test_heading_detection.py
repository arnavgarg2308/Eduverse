import unittest

from src.layout.layout_analyzer import LayoutAnalyzer
from src.heading_detection.heading_detector import HeadingDetector


class TestHeadingDetector(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.pdf_path = "sample_data/input/sample.pdf"

        layout_analyzer = LayoutAnalyzer()

        cls.layout_results = layout_analyzer.analyze_pdf(
            cls.pdf_path
        )

        heading_detector = HeadingDetector()

        cls.heading_results = heading_detector.detect_headings(
            cls.layout_results
        )

    def test_results_exist(self):

        self.assertIsNotNone(
            self.heading_results
        )

    def test_page_count(self):

        self.assertEqual(
            len(self.heading_results),
            2
        )

    def test_page_numbers(self):

        self.assertEqual(
            self.heading_results[0]["page_number"],
            1
        )

        self.assertEqual(
            self.heading_results[1]["page_number"],
            2
        )

    def test_headings_key_exists(self):

        for page in self.heading_results:

            self.assertIn(
                "headings",
                page
            )

    def test_headings_exist(self):

        total_headings = sum(
            len(page["headings"])
            for page in self.heading_results
        )

        self.assertGreater(
            total_headings,
            0
        )

    def test_heading_structure(self):

        for page in self.heading_results:

            for heading in page["headings"]:

                self.assertIn(
                    "text",
                    heading
                )

                self.assertIn(
                    "bounding_box",
                    heading
                )

                self.assertIn(
                    "height",
                    heading
                )

    def test_heading_text_exists(self):

        for page in self.heading_results:

            for heading in page["headings"]:

                self.assertTrue(
                    heading["text"].strip()
                )

    def test_heading_dimensions(self):

        for page in self.heading_results:

            for heading in page["headings"]:

                self.assertGreater(
                    heading["height"],
                    0
                )


if __name__ == "__main__":

    unittest.main()
