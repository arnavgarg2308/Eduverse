import httpx

EDUMORPH_URL = "http://localhost:8001/analyze"


async def send_pdf_to_edumorph(
    filename: str,
    file_data: bytes
):
    async with httpx.AsyncClient(timeout=120.0) as client:

        response = await client.post(
            EDUMORPH_URL,
            files={
                "file": (
                    filename,
                    file_data,
                    "application/pdf"
                )
            }
        )

        response.raise_for_status()

        return response.json()