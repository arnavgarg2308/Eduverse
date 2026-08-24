import json
from pathlib import Path

from .simplifier import EducationalSimplifier


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "ai_engine" / "test_data" / "sample_content.json"


def main():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    simplifier = EducationalSimplifier()

    result = simplifier.simplify(
        text=data["content"],
        education_level=data["education_level"]
    )

    print("\n" + "=" * 60)
    print("EDUMORPH AI - SIMPLIFICATION")
    print("=" * 60)

    print("\nTopic:", data["topic"])
    print("Subject:", data["subject"])
    print("Level:", data["education_level"])

    print("\nOriginal:\n")
    print(data["content"])

    print("\nSimplified Explanation:\n")
    print(result)


if __name__ == "__main__":
    main()