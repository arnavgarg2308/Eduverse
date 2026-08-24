import unittest

from src.layout.layout_analyzer import LayoutAnalyzer


class TestLayoutAnalyzer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pdf_path = "sample_data/input/sample.pdf"
        cls.analyzer = LayoutAnalyzer()
        cls.results = cls.analyzer.analyze_pdf(cls.pdf_path)

    def test_results_exist(self):
        self.assertIsNotNone(self.results)
        self.assertGreater(len(self.results), 0)

    def test_page_count(self):
        self.assertEqual(len(self.results), 2)

    def test_page_numbers(self):
        self.assertEqual(
            self.results[0]["page_number"],
            1
        )

        self.assertEqual(
            self.results[1]["page_number"],
            2
        )

    def test_page_dimensions(self):
        for page in self.results:
            self.assertGreater(
                page["page_width"],
                0
            )

            self.assertGreater(
                page["page_height"],
                0
            )

    def test_blocks_exist(self):
        for page in self.results:
            self.assertIn(
                "blocks",
                page
            )

            self.assertIsInstance(
                page["blocks"],
                list
            )

            self.assertGreater(
                len(page["blocks"]),
                0
            )

    def test_block_structure(self):
        for page in self.results:
            for block in page["blocks"]:

                self.assertIn(
                    "text",
                    block
                )

                self.assertIn(
                    "bounding_box",
                    block
                )

                self.assertIn(
                    "width",
                    block
                )

                self.assertIn(
                    "height",
                    block
                )

                self.assertIsInstance(
                    block["text"],
                    str
                )

    def test_block_dimensions(self):
        for page in self.results:
            for block in page["blocks"]:

                self.assertGreater(
                    block["width"],
                    0
                )

                self.assertGreater(
                    block["height"],
                    0
                )


if __name__ == "__main__":
    unittest.main()
