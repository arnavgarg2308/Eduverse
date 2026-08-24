from ai_engine.core.model import EduMorphModel


class StoryGenerator:
    """
    Creates a structured educational video script.
    FLAN-T5 is used only for the explanation.
    Python creates the final script structure.
    """

    def __init__(self, model: EduMorphModel):
        self.model = model

    def generate(
        self,
        text: str,
        topic: str,
        education_level: str = "Grade 9"
    ) -> dict:

        if not text.strip():
            raise ValueError("Educational content cannot be empty.")

        # Let FLAN-T5 handle only the explanation.
        prompt = f"""
Explain this educational content in simple language
for a {education_level} student.

Keep the important facts.
Do not invent information.
Do not copy the source word-for-word.

Topic:
{topic}

Content:
{text}

Explanation:
""".strip()

        explanation = self.model.generate(
            prompt,
            max_new_tokens=140
        )

        # Deterministic video structure.
        sentences = [
            sentence.strip()
            for sentence in text.replace("\n", " ").split(".")
            if sentence.strip()
        ]

        key_points = sentences[:4]

        script = {
            "title": topic,

            "hook": (
                f"Have you ever wondered what "
                f"{topic.lower()} means and why it matters?"
            ),

            "explanation": explanation,

            "key_points": key_points,

            "recap": (
                f"In short, {topic.lower()} is an important concept "
                f"that students should understand from the key ideas above."
            )
        }

        return script