import re

import pymupdf


class ContentDetector:

    """
    Detect content elements in a PDF.

    Detects:

    - paragraphs
    - questions

    Each detected element includes:

    - page number
    - text
    - bounding box
    """

    def detect_content(self, pdf_path):

        """
        Detect paragraphs and questions
        on every page of the PDF.
        """

        document = pymupdf.open(pdf_path)

        pages_data = []

        try:

            for page_number, page in enumerate(document):

                blocks = page.get_text("blocks")

                paragraphs = []

                questions = []

                for block in blocks:

                    x0, y0, x1, y1, text, _, _ = block

                    text = text.strip()

                    if not text:
                        continue

                    bounding_box = {
                        "x0": round(x0, 2),
                        "y0": round(y0, 2),
                        "x1": round(x1, 2),
                        "y1": round(y1, 2)
                    }

                    if self._is_question(text):

                        questions.append({
                            "text": text,
                            "bounding_box": bounding_box
                        })

                    elif self._is_paragraph(text):

                        paragraphs.append({
                            "text": text,
                            "bounding_box": bounding_box
                        })

                pages_data.append({
                    "page_number": page_number + 1,
                    "paragraphs": paragraphs,
                    "questions": questions
                })

            return pages_data

        finally:

            document.close()

    def _is_question(self, text):

        """
        Check whether a text block is likely
        to be a question.

        Numbered text is not automatically
        treated as a question because numbered
        headings can also start with:

        1.
        2.
        3.
        """

        text = " ".join(
            text.split()
        ).strip()

        if not text:
            return False

        # A question mark is a strong signal.
        if text.endswith("?"):
            return True

        question_patterns = [

            r"^(Q|Question)\s*[\d\.\s:)]*",

            r"^(Define|Explain|Describe|Discuss|Compare|"
            r"Differentiate|What|Why|How|When|Where|"
            r"Who|Give|List|State|Write)\b"
        ]

        for pattern in question_patterns:

            if re.match(
                pattern,
                text,
                re.IGNORECASE
            ):
                return True

        # Detect numbered questions such as:
        #
        # 1. Define Artificial Intelligence
        # 2. What is Machine Learning?
        # 3) Explain Deep Learning

        numbered_question_pattern = (

            r"^\d+[\.\)]\s+"

            r"(Define|Explain|Describe|Discuss|Compare|"
            r"Differentiate|What|Why|How|When|Where|"
            r"Who|Give|List|State|Write)\b"
        )

        if re.match(
            numbered_question_pattern,
            text,
            re.IGNORECASE
        ):
            return True

        return False

    def _is_paragraph(self, text):

        """
        Check whether a text block is likely
        to be a paragraph.

        Short headings and questions
        are excluded.
        """

        cleaned_text = " ".join(
            text.split()
        )

        word_count = len(
            cleaned_text.split()
        )

        # Very short text is more likely to be
        # a heading, label, or other short element.
        if word_count < 12:
            return False

        # Questions are not paragraphs.
        if self._is_question(
            cleaned_text
        ):
            return False

        # Numbered headings should not be treated
        # as paragraphs.
        if re.match(
            r"^\d+[\.\)]\s+",
            cleaned_text
        ):
            return False

        return True
