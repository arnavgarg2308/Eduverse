import easyocr


class OCREngine:
    def __init__(self, languages=None):
        """
        Initialize EasyOCR reader.

        Args:
            languages (list): Languages to detect.
        """

        if languages is None:
            languages = ["en"]

        print("Initializing EasyOCR model...")

        self.reader = easyocr.Reader(
            languages,
            gpu=False
        )

    def extract_text_from_image(self, image_path):
        """
        Extract text, bounding boxes and confidence from an image.

        Args:
            image_path (str): Path to image.

        Returns:
            list: OCR detection results.
        """

        results = self.reader.readtext(image_path)

        extracted_data = []

        for bbox, text, confidence in results:
            extracted_data.append({
                "text": text,
                "bounding_box": bbox,
                "confidence": round(float(confidence), 4)
            })

        return extracted_data

    def get_full_text(self, image_path):
        """
        Extract complete text from an image.

        Args:
            image_path (str): Path to image.

        Returns:
            str: Combined OCR text.
        """

        results = self.extract_text_from_image(image_path)

        return "\n".join(
            item["text"] for item in results
        )
