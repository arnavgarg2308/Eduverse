import re
from collections import Counter


class TopicDetector:
    """
    Detect important topics and keywords from PDF text.
    """

    def __init__(self):
        """
        Initialize common words to ignore.
        """

        self.stop_words = {
            "the", "is", "a", "an", "and", "or", "of", "to",
            "in", "on", "for", "with", "that", "this", "it",
            "as", "from", "by", "at", "be", "are", "was",
            "were", "what", "how", "uses", "using"
        }

    def extract_keywords(self, text, top_n=10):
        """
        Extract the most frequent meaningful words from text.
        """

        words = re.findall(
            r"\b[a-zA-Z]{3,}\b",
            text.lower()
        )

        meaningful_words = [
            word for word in words
            if word not in self.stop_words
        ]

        word_counts = Counter(meaningful_words)

        return word_counts.most_common(top_n)

    def detect_topics(self, pages_data, top_n=10):
        """
        Detect topics for every page.

        Args:
            pages_data (list):
                PDF page data containing extracted text.

        Returns:
            list:
                Topics and keywords for every page.
        """

        detected_topics = []

        for page in pages_data:

            text = page.get("text", "")

            keywords = self.extract_keywords(
                text,
                top_n=top_n
            )

            detected_topics.append({
                "page_number": page["page_number"],
                "keywords": keywords
            })

        return detected_topics
