from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai_engine.document_adapter import extract_text
from ai_engine.core.engine import EduMorphEngine
#from ai_engine.rag.qa import EduMorphRAG


app = FastAPI(
    title="EduMorph AI Engine",
    version="1.0.0",
)

# Load the shared FLAN-T5 model once.
engine = EduMorphEngine()

# RAG will reuse the same model.
#rag = EduMorphRAG(engine.model)


class EducationalRequest(BaseModel):
    content: str
    topic: str = "General"
    education_level: str = "Grade 9"
    number_of_questions: int = 3

class DocumentRequest(BaseModel):
    document: dict
    topic: str = "General"
    education_level: str = "Grade 9"
    number_of_questions: int = 3

#class RAGRequest(BaseModel):
  #  chunks: list[str]
   # question: str
   # education_level: str = "Grade 9"
   # top_k: int = 3


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

        # AI Engine se processing
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
        result = engine.process(
            content=request.content,
            topic=request.topic,
            education_level=request.education_level,
            number_of_questions=request.number_of_questions,
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


#@app.post("/rag")
#def rag_answer(request: RAGRequest):

    if not request.chunks:
        raise HTTPException(
            status_code=400,
            detail="At least one document chunk is required."
        )

    try:
        rag.add_document(request.chunks)

        result = rag.answer(
            query=request.question,
            education_level=request.education_level,
            top_k=request.top_k,
        )

        return {
            "success": True,
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )