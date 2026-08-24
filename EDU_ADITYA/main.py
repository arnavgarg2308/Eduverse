import sys

from src.pipeline.document_analyzer import DocumentAnalyzer


def main():

    if len(sys.argv) < 2:

        print("Usage:")
        print("python main.py <pdf_path> [output_path]")

        sys.exit(1)

    pdf_path = sys.argv[1]

    if len(sys.argv) >= 3:

        output_path = sys.argv[2]

    else:

        output_path = (
            "sample_data/output/document_analysis.json"
        )

    analyzer = DocumentAnalyzer()

    print()
    print("========== EDUMORPH DOCUMENT INTELLIGENCE ==========")
    print()
    print(f"Analyzing PDF: {pdf_path}")
    print()

    try:

        document_structure = analyzer.analyze(
            pdf_path,
            output_path
        )

        print("Analysis completed successfully!")
        print()

        print(
            f"File Name: "
            f"{document_structure['file_name']}"
        )

        print(
            f"Page Count: "
            f"{document_structure['page_count']}"
        )

        print()

        print(f"Output saved to: {output_path}")

    except FileNotFoundError as error:

        print()
        print(f"Error: {error}")

        sys.exit(1)

    except Exception as error:

        print()
        print("An unexpected error occurred:")
        print(error)

        sys.exit(1)


if __name__ == "__main__":

    main()
