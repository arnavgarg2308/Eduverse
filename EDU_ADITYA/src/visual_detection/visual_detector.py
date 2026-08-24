import pymupdf


class VisualDetector:

    """
    Detect visual elements in a PDF.

    Initial version detects:

    - embedded images
    - vector drawings

    Vector drawings will later be classified into:

    - diagrams
    - flowcharts
    """

    def detect_visuals(self, pdf_path):

        """
        Detect visual elements on every page.

        Returns a list containing visual data
        grouped by page.
        """

        document = pymupdf.open(pdf_path)

        pages_data = []

        try:

            for page_number, page in enumerate(document):

                images = self._detect_images(
                    page
                )

                drawings = self._detect_drawings(
                    page
                )

                pages_data.append({

                    "page_number": page_number + 1,

                    "images": images,

                    "drawings": drawings

                })

            return pages_data

        finally:

            document.close()

    def _detect_images(
        self,
        page
    ):

        """
        Detect embedded images and their
        bounding boxes.
        """

        detected_images = []

        image_list = page.get_images(
            full=True
        )

        seen_images = set()

        image_number = 1

        for image in image_list:

            xref = image[0]

            image_rectangles = page.get_image_rects(
                xref
            )

            for rect in image_rectangles:

                image_key = (

                    round(rect.x0, 2),
                    round(rect.y0, 2),
                    round(rect.x1, 2),
                    round(rect.y1, 2)

                )

                if image_key in seen_images:

                    continue

                seen_images.add(
                    image_key
                )

                detected_images.append({

                    "image_number": image_number,

                    "bounding_box": {

                        "x0": round(rect.x0, 2),

                        "y0": round(rect.y0, 2),

                        "x1": round(rect.x1, 2),

                        "y1": round(rect.y1, 2)

                    }

                })

                image_number += 1

        return detected_images

    def _detect_drawings(
        self,
        page
    ):

        """
        Detect vector drawings.

        These can include:

        - diagram shapes
        - flowchart boxes
        - arrows
        - lines
        - other vector graphics

        Later we will group and classify them.
        """

        drawings = page.get_drawings()

        detected_drawings = []

        for drawing_number, drawing in enumerate(
            drawings,
            start=1
        ):

            rect = drawing.get(
                "rect"
            )

            if rect is None:

                continue

            detected_drawings.append({

                "drawing_number": drawing_number,

                "bounding_box": {

                    "x0": round(rect.x0, 2),

                    "y0": round(rect.y0, 2),

                    "x1": round(rect.x1, 2),

                    "y1": round(rect.y1, 2)

                },

                "item_count": len(
                    drawing.get(
                        "items",
                        []
                    )
                )

            })

        return detected_drawings
