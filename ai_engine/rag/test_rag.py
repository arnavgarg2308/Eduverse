from ai_engine.core.model import EduMorphModel
from ai_engine.rag.qa import EduMorphRAG


def main():

    chunks = [
        "Biodiversity is the variety of living organisms on Earth.",
        "Algae contribute oxygen, while fungi and bacteria decompose organic matter.",
        "Birds, bees, and bats help pollinate plants.",
        "Humans depend on biodiversity for food, medicines, shelter, and livelihoods.",
        "Classification helps organize living organisms based on shared characteristics."
    ]

    model = EduMorphModel()

    rag = EduMorphRAG(model)

    rag.add_document(chunks)

    query = "Why is biodiversity important?"

    result = rag.answer(
        query=query,
        education_level="Grade 9",
        top_k=3
    )

    print("\nQUESTION:")
    print(result["question"])

    print("\nANSWER:")
    print(result["answer"])

    print("\nRETRIEVED SOURCES:")

    for source in result["sources"]:
        print(
            f"\nScore: {source['score']:.3f}"
        )
        print(source["chunk"])


if __name__ == "__main__":
    main()