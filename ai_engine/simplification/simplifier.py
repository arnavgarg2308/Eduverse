from ai_engine.core.model import EduMorphModel


class EducationalSimplifier:
    """
    Educational text simplification module.
    Uses the shared EduMorph FLAN-T5 model.
    """

    def __init__(self, model: EduMorphModel):
        self.model = model

    def simplify(
        self,
        text: str,
        education_level: str = "Grade 9"
    ) -> str:

        if not text or not text.strip():
            raise ValueError(
                "Input educational text cannot be empty."
            )

        prompt = f"""
Simplify the following educational content for a {education_level} student.

Requirements:
- Explain the main idea clearly.
- Use simple language.
- Preserve important facts.
- Do not invent information.
- Do not change the meaning.

Educational content:
{text}

Simple explanation:
""".strip()

        return self.model.generate(
            prompt,
            max_new_tokens=150
        )