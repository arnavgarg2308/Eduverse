import unittest

from src.pdf_reader.reader import PDFReader
from src.topic_detection.topic_detector import TopicDetector


class TestTopicDetector(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.pdf_path = "sample_data/input/sample.pdf"

        pdf_reader = PDFReader(cls.pdf_path)

        document_info = pdf_reader.get_document_info()

        cls.pages_data = document_info["pages"]

        topic_detector = TopicDetector()

        cls.results = topic_detector.detect_topics(
            cls.pages_data,
            top_n=10
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

    def test_keywords_key_exists(self):

        for page in self.results:

            self.assertIn(
                "keywords",
                page
            )

    def test_keywords_exist(self):

        total_keywords = sum(
            len(page["keywords"])
            for page in self.results
        )

        self.assertGreater(
            total_keywords,
            0
        )

    def test_keyword_structure(self):

        for page in self.results:

            for keyword_data in page["keywords"]:

                self.assertIsInstance(
                    keyword_data,
                    tuple
                )

                self.assertEqual(
                    len(keyword_data),
                    2
                )

    def test_keyword_text_is_valid(self):

        for page in self.results:

            for keyword, count in page["keywords"]:

                self.assertIsInstance(
                    keyword,
                    str
                )

                self.assertTrue(
                    keyword.strip()
                )

    def test_keyword_count_is_valid(self):

        for page in self.results:

            for keyword, count in page["keywords"]:

                self.assertIsInstance(
                    count,
                    int
                )

                self.assertGreater(
                    count,
                    0
                )

    def test_top_n_limit(self):

        for page in self.results:

            self.assertLessEqual(
                len(page["keywords"]),
                10
            )


if __name__ == "__main__":

    unittest.main()
