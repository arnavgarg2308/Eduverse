from src.ocr.pdf_ocr import PDFOCR


def main():
    pdf_path = "sample_data/input/sample.pdf"

    ocr = PDFOCR()

    results = ocr.extract_text_from_pdf(pdf_path)

    print("\n========== OCR RESULTS ==========\n")

    for page in results:
        print(f"PAGE: {page['page_number']}")

        print("\nExtracted Text:\n")
        print(page["text"])

        print("\nNumber of OCR blocks:")
        print(len(page["ocr_blocks"]))

        print("\n" + "=" * 40 + "\n")


if __name__ == "__main__":
    main()
