import re


class DifficultyPredictor:
    """
    Baseline difficulty estimator.

    This is NOT a trained ML model yet.
    It is a transparent baseline based on
    lexical and structural complexity.
    """

    DIFFICULT_WORDS = {
        "classification",
        "evolutionary",
        "biodiversity",
        "heterotrophic",
        "prokaryotic",
        "eukaryotic",
        "photosynthesis",
        "normalization",
        "dependency",
        "algorithmic"
    }

    def predict(self, text: str) -> dict:

        words = re.findall(
            r"\b[a-zA-Z]+\b",
            text.lower()
        )

        if not words:
            return {
                "difficulty": "unknown",
                "score": 0.0
            }

        avg_word_length = (
            sum(len(word) for word in words)
            / len(words)
        )

        difficult_count = sum(
            1 for word in words
            if word in self.DIFFICULT_WORDS
        )

        score = (
            min(avg_word_length / 8, 1.0) * 0.4
            +
            min(difficult_count / 10, 1.0) * 0.6
        )

        if score < 0.30:
            level = "Beginner"
        elif score < 0.60:
            level = "Intermediate"
        else:
            level = "Advanced"

        return {
            "difficulty": level,
            "score": round(score, 3)
        }
        