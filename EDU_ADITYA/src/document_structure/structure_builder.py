class DocumentStructureBuilder:

    """
    Build a structured representation of a document
    using headings, topics, tables, paragraphs,
    questions, and visual elements.

    Existing keys such as headings, topics, and tables
    are preserved for backward compatibility.

    The unified "elements" list contains all detected
    content in reading order.
    """

    def build_structure(

        self,

        document_info,

        heading_data,

        topic_data,

        table_data,

        content_data=None,

        visual_data=None

    ):

        """
        Combine results from different modules into
        one document structure.
        """

        pages = document_info["pages"]

        structure_pages = []

        for page in pages:

            page_number = page["page_number"]

            page_headings = self._get_page_data(

                heading_data,

                page_number,

                "headings"

            )

            page_topics = self._get_page_data(

                topic_data,

                page_number,

                "keywords"

            )

            page_tables = self._get_page_data(

                table_data,

                page_number,

                "tables"

            )

            page_content = self._get_page_item(

                content_data,

                page_number

            )

            page_paragraphs = page_content.get(

                "paragraphs",

                []

            )

            page_questions = page_content.get(

                "questions",

                []

            )

            page_visuals = self._get_page_item(

                visual_data,

                page_number

            )

            page_images = page_visuals.get(

                "images",

                []

            )

            page_drawings = page_visuals.get(

                "drawings",

                []

            )

            elements = self._build_elements(

                page_headings,

                page_paragraphs,

                page_questions,

                page_tables,

                page_images,

                page_drawings

            )

            structure_pages.append({

                "page_number": page_number,

                "text": page["text"],

                "headings": page_headings,

                "topics": page_topics,

                "tables": page_tables,

                "elements": elements

            })

        return {

            "file_name": document_info["file_name"],

            "page_count": document_info["page_count"],

            "pages": structure_pages

        }

    def _get_page_data(

        self,

        data_list,

        page_number,

        key

    ):

        """
        Get specific list data for a page.
        """

        if not data_list:

            return []

        for item in data_list:

            if item.get("page_number") == page_number:

                return item.get(

                    key,

                    []

                )

        return []

    def _get_page_item(

        self,

        data_list,

        page_number

    ):

        """
        Get the complete data dictionary
        for a specific page.
        """

        if not data_list:

            return {}

        for item in data_list:

            if item.get("page_number") == page_number:

                return item

        return {}

    def _build_elements(

        self,

        headings,

        paragraphs,

        questions,

        tables,

        images,

        drawings

    ):

        """
        Convert all detected page content into
        one unified elements list.

        Duplicate or overlapping text elements
        are removed.

        Every element is then sorted into
        reading order.
        """

        elements = []

        # Add headings first.
        # Headings have priority over questions
        # when the same text appears in both lists.

        for heading in headings:

            text = heading.get(

                "text",

                ""

            ).strip()

            bounding_box = heading.get(

                "bounding_box",

                {}

            )

            elements.append({

                "type": "heading",

                "text": text,

                "bounding_box": bounding_box

            })

        # Add paragraphs.

        for paragraph in paragraphs:

            text = paragraph.get(

                "text",

                ""

            ).strip()

            bounding_box = paragraph.get(

                "bounding_box",

                {}

            )

            if self._is_duplicate_text_element(

                elements,

                text,

                bounding_box

            ):

                continue

            elements.append({

                "type": "paragraph",

                "text": text,

                "bounding_box": bounding_box

            })

        # Add questions.
        # Skip questions that are already
        # represented as headings.

        for question in questions:

            text = question.get(

                "text",

                ""

            ).strip()

            bounding_box = question.get(

                "bounding_box",

                {}

            )

            if self._is_duplicate_text_element(

                elements,

                text,

                bounding_box

            ):

                continue

            elements.append({

                "type": "question",

                "text": text,

                "bounding_box": bounding_box

            })

        # Add tables.

        for table in tables:

            bounding_box = table.get(

                "bounding_box",

                {}

            )

            elements.append({

                "type": "table",

                "table_number": table.get(

                    "table_number"

                ),

                "data": table.get(

                    "data",

                    []

                ),

                "bounding_box": bounding_box

            })

        # Add images.

        for image in images:

            bounding_box = image.get(

                "bounding_box",

                {}

            )

            elements.append({

                "type": "image",

                "image_number": image.get(

                    "image_number"

                ),

                "bounding_box": bounding_box

            })

        # Add drawings.

        for drawing in drawings:

            bounding_box = drawing.get(

                "bounding_box",

                {}

            )

            elements.append({

                "type": "drawing",

                "drawing_number": drawing.get(

                    "drawing_number"

                ),

                "item_count": drawing.get(

                    "item_count",

                    0

                ),

                "bounding_box": bounding_box

            })

        # Sort all elements from top to bottom.
        # If two elements have the same vertical
        # position, sort from left to right.

        elements.sort(

            key=lambda element: (

                self._get_y_position(

                    element.get(

                        "bounding_box",

                        {}

                    )

                ),

                self._get_x_position(

                    element.get(

                        "bounding_box",

                        {}

                    )

                )

            )

        )

        return elements

    def _is_duplicate_text_element(

        self,

        elements,

        text,

        bounding_box

    ):

        """
        Check whether a text element already exists.

        A duplicate is identified primarily by:

        - same normalized text
        - same or nearly identical position
        """

        normalized_text = self._normalize_text(

            text

        )

        for element in elements:

            existing_text = self._normalize_text(

                element.get(

                    "text",

                    ""

                )

            )

            if not existing_text:

                continue

            if existing_text != normalized_text:

                continue

            existing_box = element.get(

                "bounding_box",

                {}

            )

            if self._boxes_overlap(

                existing_box,

                bounding_box

            ):

                return True

        return False

    def _normalize_text(

        self,

        text

    ):

        """
        Normalize text for duplicate comparison.
        """

        return " ".join(

            text.lower().split()

        )

    def _boxes_overlap(

        self,

        box_one,

        box_two

    ):

        """
        Check whether two bounding boxes
        represent approximately the same area.
        """

        if not box_one or not box_two:

            return False

        tolerance = 2

        return (

            abs(

                box_one.get(

                    "x0",

                    0

                ) - box_two.get(

                    "x0",

                    0

                )

            ) <= tolerance

            and

            abs(

                box_one.get(

                    "y0",

                    0

                ) - box_two.get(

                    "y0",

                    0

                )

            ) <= tolerance

            and

            abs(

                box_one.get(

                    "x1",

                    0

                ) - box_two.get(

                    "x1",

                    0

                )

            ) <= tolerance

            and

            abs(

                box_one.get(

                    "y1",

                    0

                ) - box_two.get(

                    "y1",

                    0

                )

            ) <= tolerance

        )

    def _get_y_position(

        self,

        bounding_box

    ):

        """
        Get the vertical position of an element.
        """

        if not bounding_box:

            return 0

        return bounding_box.get(

            "y0",

            0

        )

    def _get_x_position(

        self,

        bounding_box

    ):

        """
        Get the horizontal position of an element.
        """

        if not bounding_box:

            return 0

        return bounding_box.get(

            "x0",

            0

        )
