import re

from ai_engine.core.model import EduMorphModel


class StoryGenerator:
    """
    Creates a structured educational video script.

    The AI creates a clean educational explanation.
    Python then converts it into multiple video-ready scenes.
    """

    def __init__(self, model: EduMorphModel):
        self.model = model

    def generate(
        self,
        text: str,
        topic: str,
        education_level: str = "Grade 3"
    ) -> dict:

        if not text or not text.strip():
            raise ValueError("Educational content cannot be empty.")

        # ------------------------------------------------
        # 1. Clean extracted PDF text
        # ------------------------------------------------
        cleaned_text = re.sub(r"\s+", " ", text).strip()

        # Remove some common PDF noise
        cleaned_text = re.sub(
            r"Reprint\s+\d{4}-\d{2}",
            "",
            cleaned_text,
            flags=re.IGNORECASE
        )

        # Keep input manageable for the model
        content_for_ai = cleaned_text[:6000]

        # ------------------------------------------------
        # 2. Generate a structured lesson explanation
        # ------------------------------------------------
        prompt = f"""
You are an expert primary school teacher.

Read the educational content below and create a clear,
simple explanation for a {education_level} student.

IMPORTANT RULES:
- Detect the real topic from the content if the provided topic is "General".
- Use the same language as the educational content.
- Do not invent facts.
- Remove repeated PDF text and page headers.
- Focus only on the actual lesson.
- Explain the main ideas in simple child-friendly language.
- Divide the explanation into 5 to 8 short learning points.
- Each learning point should be suitable for one educational video scene.
- Do not copy the entire source.
- Do not include page numbers, "Reprint", or textbook metadata.

Provided topic: {topic}

Educational content:
{content_for_ai}

Write only the educational explanation:
""".strip()

        explanation = self.model.generate(
            prompt,
            max_new_tokens=500
        ).strip()

        # ------------------------------------------------
        # 3. Split AI explanation into usable points
        # Supports Hindi । and English .
        # ------------------------------------------------
        raw_points = re.split(r"[।.!?\n]+", explanation)

        points = []

        for point in raw_points:
            point = point.strip(" -•\t")

            if len(point) >= 20:
                points.append(point)

        # Fallback if model generates too little output
        if len(points) < 2:
            raw_sentences = re.split(r"[।.!?\n]+", cleaned_text)

            points = [
                sentence.strip()
                for sentence in raw_sentences
                if len(sentence.strip()) >= 20
            ][:6]

        # ------------------------------------------------
        # 4. Limit points for a reasonable video
        # ------------------------------------------------
        points = points[:8]

        # ------------------------------------------------
        # 5. Detect a better title
        # ------------------------------------------------
        actual_topic = topic

        if not topic or topic.lower() == "general":
            actual_topic = points[0][:60] if points else "Educational Lesson"

        # ------------------------------------------------
        # 6. Create multiple video scenes
        # ------------------------------------------------
        scenes = []

        for index, point in enumerate(points, start=1):

            scene = {
                "scene_number": index,
                "title": (
                    actual_topic
                    if index == 1
                    else f"Learning Point {index}"
                ),
                "narration": point,
                "visual_description": (
                    f"Create a colorful, child-friendly educational "
                    f"animation that visually explains: {point}"
                )
            }

            scenes.append(scene)

        # ------------------------------------------------
        # 7. Final script
        # ------------------------------------------------
        script = {
            "title": actual_topic,
            "education_level": education_level,
            "explanation": explanation,
            "key_points": points,
            "scenes": scenes,
            "recap": (
                points[-1]
                if points
                else "Review the important ideas from this lesson."
            )
        }

        return script