import unittest

from src.table_detection.table_detector import TableDetector


class TestTableDetector(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.pdf_path = "sample_data/input/sample.pdf"

        table_detector = TableDetector()

        cls.results = table_detector.detect_tables(
            cls.pdf_path
        )

    def test_results_exist(self):

        self.assertIsNotNone(
            self.results
        )

    def test_page_count(self):

        self.assertEqual(
            len(self.results),
            2
        )

    def test_page_numbers(self):

        self.assertEqual(
            self.results[0]["page_number"],
            1
        )

        self.assertEqual(
            self.results[1]["page_number"],
            2
        )

    def test_page_structure(self):

        for page in self.results:

            self.assertIn(
                "page_number",
                page
            )

            self.assertIn(
                "table_count",
                page
            )

            self.assertIn(
                "tables",
                page
            )

    def test_table_count_is_valid(self):

        for page in self.results:

            self.assertIsInstance(
                page["table_count"],
                int
            )

            self.assertGreaterEqual(
                page["table_count"],
                0
            )

    def test_table_count_matches_tables(self):

        for page in self.results:

            self.assertEqual(
                page["table_count"],
                len(page["tables"])
            )

    def test_tables_is_list(self):

        for page in self.results:

            self.assertIsInstance(
                page["tables"],
                list
            )

    def test_table_structure_if_present(self):

        for page in self.results:

            for table in page["tables"]:

                self.assertIn(
                    "table_number",
                    table
                )

                self.assertIn(
                    "data",
                    table
                )

                self.assertIn(
                    "bounding_box",
                    table
                )

    def test_table_numbers_if_present(self):

        for page in self.results:

            for index, table in enumerate(
                page["tables"],
                start=1
            ):

                self.assertEqual(
                    table["table_number"],
                    index
                )

    def test_bounding_box_structure_if_present(self):

        expected_keys = [
            "x0",
            "y0",
            "x1",
            "y1"
        ]

        for page in self.results:

            for table in page["tables"]:

                bounding_box = table["bounding_box"]

                for key in expected_keys:

                    self.assertIn(
                        key,
                        bounding_box
                    )


if __name__ == "__main__":

    unittest.main()
