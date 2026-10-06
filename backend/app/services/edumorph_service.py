import httpx


AI_ENGINE_URL = "http://127.0.0.1:8002/process"
QUIZ_AI_ENGINE_URL = "http://127.0.0.1:8002/generate-quiz"


async def send_text_to_edumorph(
    text: str,
    topic: str = "General",
    education_level: str = "General",
    number_of_questions: int = 3,
    headings: list = None,
    content_start: int = 0,
):
    async with httpx.AsyncClient(timeout=300.0) as client:
        response = await client.post(
            AI_ENGINE_URL,
            json={
                "content": text,
                "topic": topic,
                "education_level": education_level,
                "number_of_questions": number_of_questions,
                "headings": headings or [],
                "content_start": content_start,
            },
        )

        response.raise_for_status()

        return response.json()


async def generate_quiz_from_text(
    text: str,
    education_level: str = "General",
    number_of_questions: int = 3,
):
    if not text or not text.strip():
        raise ValueError(
            "Educational content cannot be empty."
        )

    if number_of_questions < 1:
        raise ValueError(
            "number_of_questions must be at least 1."
        )

    async with httpx.AsyncClient(timeout=300.0) as client:

        response = await client.post(
            QUIZ_AI_ENGINE_URL,
            json={
                "content": text,
                "education_level": education_level,
                "number_of_questions": number_of_questions,
            },
        )

        response.raise_for_status()

        return response.json()