import json


def load_document(document_path):

    with open(
        document_path,
        "r",
        encoding="utf-8"
    ) as file:

        document_data = json.load(file)

    return document_data


def extract_text(document_data):

    text_parts = []

    if isinstance(document_data, dict):

        def find_text(data):

            if isinstance(data, dict):

                for key, value in data.items():

                    if key.lower() in [
                        "text",
                        "content",
                        "paragraph",
                        "body"
                    ] and isinstance(value, str):

                        text_parts.append(value)

                    find_text(value)

            elif isinstance(data, list):

                for item in data:

                    find_text(item)

        find_text(document_data)

    return "\n".join(text_parts)