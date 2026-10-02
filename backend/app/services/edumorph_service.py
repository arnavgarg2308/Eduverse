import httpx

AI_ENGINE_URL = "http://127.0.0.1:8002/process"


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
            }
        )
        response.raise_for_status()
        return response.json()
