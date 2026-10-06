from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ai_engine.document_adapter import extract_text
from ai_engine.core.engine import EduMorphEngine


app = FastAPI(
    title="EduMorph AI Engine",
    version="1.0.0",
)

# Load the shared FLAN-T5 model once.
engine = EduMorphEngine()


class EducationalRequest(BaseModel):
    content: str
    topic: str = "General"
    education_level: str = "General"
    number_of_questions: int = 3
    headings: list = []
    content_start: int = 0


class DocumentRequest(BaseModel):
    document: dict
    topic: str = "General"
    education_level: str = "General"
    number_of_questions: int = 3


class QuizRequest(BaseModel):
    content: str
    education_level: str = "General"
    number_of_questions: int = 3


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "EduMorph AI Engine"
    }


@app.post("/process-document")
def process_document(request: DocumentRequest):

    try:

        # Document Analyzer ke JSON se actual educational text nikalo
        content = extract_text(request.document)

        if not content.strip():
            raise HTTPException(
                status_code=400,
                detail="No educational text found in document JSON"
            )

        # Existing complete AI processing pipeline.
        result = engine.process(
            content=content,
            topic=request.topic,
            education_level=request.education_level,
            number_of_questions=request.number_of_questions,
        )

        return {
            "success": True,
            "topic": request.topic,
            "education_level": request.education_level,
            "extracted_content": content,
            "result": result,
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


@app.post("/process")
def process_content(request: EducationalRequest):

    if not request.content.strip():
        raise HTTPException(
            status_code=400,
            detail="content cannot be empty"
        )

    try:

        # Existing endpoint.
        # Do not change its behavior because other features
        # already use this complete processing pipeline.
        result = engine.process(
            content=request.content,
            topic=request.topic,
            education_level=request.education_level,
            number_of_questions=request.number_of_questions,
            headings=request.headings,
            content_start=request.content_start,
        )

        return {
            "success": True,
            "topic": request.topic,
            "education_level": request.education_level,
            "result": result,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


@app.post("/generate-quiz")
def generate_quiz(request: QuizRequest):

    if not request.content.strip():
        raise HTTPException(
            status_code=400,
            detail="content cannot be empty"
        )

    if request.number_of_questions < 1:
        raise HTTPException(
            status_code=400,
            detail="number_of_questions must be at least 1"
        )

    try:

        quiz = engine.quiz_generator.generate(
            text=request.content,
            education_level=request.education_level,
            number_of_questions=request.number_of_questions,
        )

        return {
            "success": True,
            "education_level": request.education_level,
            "result": quiz,
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=422,
            detail=str(exc)
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Quiz generation failed: {str(exc)}"
        )

