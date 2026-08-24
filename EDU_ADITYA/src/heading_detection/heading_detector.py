import re


class HeadingDetector:
    """
    Detect headings from PDF layout blocks using
    position, size, and text patterns.
    """

    def is_heading(self, block):
        """
        Determine whether a text block is likely a heading.
        """

        text = block["text"].strip()

        # Ignore empty text
        if not text:
            return False

        # Ignore long paragraphs
        if len(text) > 100:
            return False

        # Heading pattern:
        # Examples:
        # "1. Introduction"
        # "2. Machine Learning"
        # "3. Introduction to Deep Learning"
        numbered_heading = re.match(
            r"^\d+\.\s+[A-Z]",
            text
        )

        # Short title-like text
        short_text = (
            len(text) <= 50
            and "\n" not in text
        )

        # A block with a larger height is likely a title/heading
        large_block = block["height"] >= 20

        # Detect numbered headings
        if numbered_heading and large_block:
            return True

        # Detect short titles such as:
        # "Introduction to Artificial Intelligence"
        # "Deep Learning"
        # "Exercises"
        if short_text and large_block:
            return True

        return False

    def detect_headings(self, layout_pages):
        """
        Detect headings from layout analysis results.

        Args:
            layout_pages (list):
                Output from LayoutAnalyzer.analyze_pdf().

        Returns:
            list:
                Detected headings grouped by page.
        """

        heading_pages = []

        for page in layout_pages:

            page_headings = []

            for block in page["blocks"]:

                if self.is_heading(block):

                    page_headings.append({
                        "text": block["text"],
                        "bounding_box": block["bounding_box"],
                        "width": block["width"],
                        "height": block["height"]
                    })

            heading_pages.append({
                "page_number": page["page_number"],
                "headings": page_headings
            })

        return heading_pages
