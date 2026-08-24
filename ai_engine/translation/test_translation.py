from .translator import RegionalTranslator


def main():

    translator = RegionalTranslator()

    text = (
        "Biodiversity refers to the variety of living organisms "
        "on Earth. Different organisms perform different roles "
        "in ecosystems."
    )

    result = translator.translate(
        text=text,
        target_language="hindi"
    )

    print("\nEnglish:")
    print(text)

    print("\nHindi:")
    print(result)


if __name__ == "__main__":
    main()