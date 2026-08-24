from ai_engine.core.model import EduMorphModel


class QuizGenerator:
    """
    Educational quiz-generation module.
    Uses the shared EduMorph FLAN-T5 model.
    """

    def __init__(self, model: EduMorphModel):
        self.model = model

    def generate(
        self,
        text: str,
        education_level: str = "Grade 9",
        number_of_questions: int = 3
    ) -> str:

        if not text or not text.strip():
            raise ValueError(
                "Input educational text cannot be empty."
            )

        prompt = f"""
Create {number_of_questions} multiple-choice questions
from the educational content below for a {education_level} student.

For every question provide:

QUESTION:
A:
B:
C:
D:
ANSWER:
EXPLANATION:

Use only the supplied content.
Do not invent facts.

Educational content:
{text}
""".strip()

        return self.model.generate(
            prompt,
            max_new_tokens=300
        )