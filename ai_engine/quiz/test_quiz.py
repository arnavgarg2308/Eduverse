from .quiz_generator import QuizGenerator


def main():
    generator = QuizGenerator()

    text = """
    Normalization in a DBMS is the process of organizing
    data to reduce redundancy and improve data integrity.

    First Normal Form requires atomic values and no
    repeating groups.

    Second Normal Form requires First Normal Form and
    removal of partial dependency.
    """

    result = generator.generate(
        text=text,
        education_level="B.Tech",
        number_of_questions=3
    )

    print("\nGenerated Quiz:\n")
    print(result)


if __name__ == "__main__":
    main()