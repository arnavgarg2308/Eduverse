from ai_engine.core.model import EduMorphModel
from ai_engine.simplification.simplifier import EducationalSimplifier
from ai_engine.quiz.quiz_generator import QuizGenerator
from ai_engine.story.story_generator import StoryGenerator
from ai_engine.difficulty.difficulty_predictor import DifficultyPredictor


class EduMorphEngine:

    def __init__(self):
        print("Initializing EduMorph AI Engine...")

        # Load FLAN-T5 only once
        self.model = EduMorphModel()

        # All generative modules share the same model
        self.simplifier = EducationalSimplifier(self.model)
        self.quiz_generator = QuizGenerator(self.model)
        self.story_generator = StoryGenerator(self.model)

        # Difficulty predictor does not use FLAN-T5
        self.difficulty_predictor = DifficultyPredictor()

        print("EduMorph AI Engine ready.")

    def process(
        self,
        content: str,
        topic: str,
        education_level: str = "General",
        number_of_questions: int = 3,
        headings: list = None,
        content_start: int = 0,
    ) -> dict:

        if not content or not content.strip():
            raise ValueError(
                "Educational content cannot be empty."
            )

        simplified = self.simplifier.simplify(
            content,
            education_level
        )

        quiz = self.quiz_generator.generate(
            content,
            education_level,
            number_of_questions
        )

        story = self.story_generator.generate(
            text=content,
            topic=topic,
            education_level=education_level,
            headings=headings or [],
            content_start=content_start,
        )

        difficulty = self.difficulty_predictor.predict(
            content
        )

        return {
            "simplified_explanation": simplified,
            "quiz": quiz,
            "story_script": story,
            "difficulty": difficulty
        }
