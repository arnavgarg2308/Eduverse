import json
import os
import unittest

from src.output.json_writer import JSONWriter


class TestJSONWriter(unittest.TestCase):

    def setUp(self):

        self.output_path = (
            "sample_data/output/test_document_analysis.json"
        )

        self.sample_data = {
            "file_name": "test.pdf",
            "page_count": 2,
            "pages": [
                {
                    "page_number": 1,
                    "text": "Sample page one",
                    "headings": [],
                    "topics": [],
                    "tables": []
                },
                {
                    "page_number": 2,
                    "text": "Sample page two",
                    "headings": [],
                    "topics": [],
                    "tables": []
                }
            ]
        }

        self.writer = JSONWriter()

        # Remove old test file before each test
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

    def tearDown(self):

        # Remove test file after each test
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

    def test_writer_exists(self):

        self.assertIsNotNone(
            self.writer
        )

    def test_save_returns_output_path(self):

        result = self.writer.save(
            self.sample_data,
            self.output_path
        )

        self.assertEqual(
            result,
            self.output_path
        )

    def test_json_file_is_created(self):

        self.writer.save(
            self.sample_data,
            self.output_path
        )

        self.assertTrue(
            os.path.exists(self.output_path)
        )

    def test_json_content_is_correct(self):

        self.writer.save(
            self.sample_data,
            self.output_path
        )

        with open(
            self.output_path,
            "r",
            encoding="utf-8"
        ) as json_file:

            loaded_data = json.load(
                json_file
            )

        self.assertEqual(
            loaded_data,
            self.sample_data
        )

    def test_json_is_valid(self):

        self.writer.save(
            self.sample_data,
            self.output_path
        )

        with open(
            self.output_path,
            "r",
            encoding="utf-8"
        ) as json_file:

            loaded_data = json.load(
                json_file
            )

        self.assertIsInstance(
            loaded_data,
            dict
        )

    def test_output_directory_is_created(self):

        output_path = (
            "sample_data/output/test_directory/"
            "test_output.json"
        )

        if os.path.exists(output_path):
            os.remove(output_path)

        self.writer.save(
            self.sample_data,
            output_path
        )

        self.assertTrue(
            os.path.exists(output_path)
        )

        if os.path.exists(output_path):
            os.remove(output_path)


if __name__ == "__main__":

    unittest.main()
