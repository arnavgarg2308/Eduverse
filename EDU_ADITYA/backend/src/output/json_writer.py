import json
import os


class JSONWriter:

    """
    Save document analysis results as a JSON file.
    """

    def save(
        self,
        data,
        output_path="sample_data/output/document_analysis.json"
    ):
        """
        Save data to a formatted JSON file.
        """

        output_directory = os.path.dirname(output_path)

        if output_directory:
            os.makedirs(
                output_directory,
                exist_ok=True
            )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as json_file:

            json.dump(
                data,
                json_file,
                indent=4,
                ensure_ascii=False
            )

        return output_path
