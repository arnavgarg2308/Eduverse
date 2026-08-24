import json
import os
import shutil
import uuid
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from src.pipeline.document_analyzer import DocumentAnalyzer

#from app.database.mongodb import (
 #   connect_to_mongo,
  #  close_mongo_connection,
#)
from app.routes.auth import router as auth_router
from app.routes.course import router as course_router

AI_ENGINE_URL = "http://127.0.0.1:8002/process-document"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await connect_to_mongo()

    yield

    # await close_mongo_connection()


app = FastAPI(
    title="AI Learning Platform API",
    version="1.0.0",
    lifespan=lifespan
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create folders for EduMorph
UPLOAD_DIRECTORY = "uploads"
OUTPUT_DIRECTORY = "output"

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)


# Authentication & Course routes
app.include_router(auth_router)
app.include_router(course_router)


@app.get("/")
def home():
    return {
        "message": "AI Learning Platform Backend Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ==========================================
# EduMorph PDF Analysis Route
# ==========================================

@app.post("/analyze")
async def analyze_pdf(
    file: UploadFile = File(...),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file was uploaded",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed",
        )

    file_id = str(uuid.uuid4())
    input_filename = f"{file_id}_{file.filename}"
    input_path = os.path.join(UPLOAD_DIRECTORY, input_filename)
    original_name = os.path.splitext(file.filename)[0]
    output_filename = f"{original_name}_analysis.json"
    output_path = os.path.join(OUTPUT_DIRECTORY, output_filename)
    final_output_filename = f"{original_name}_ai_output.json"
    final_output_path = os.path.join(OUTPUT_DIRECTORY, final_output_filename)

    try:
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        analyzer = DocumentAnalyzer()
        analyzer.analyze(input_path, output_path)

        with open(output_path, "r", encoding="utf-8") as json_file:
            document_json = json.load(json_file)

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                AI_ENGINE_URL,
                json={
                    "document": document_json,
                    "topic": "General",
                    "education_level": "Grade 9",
                    "number_of_questions": 3,
                },
                timeout=120.0,
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail=f"AI Engine Error: {response.text}",
            )

        ai_result = response.json()

        with open(final_output_path, "w", encoding="utf-8") as final_file:
            json.dump(ai_result, final_file, indent=4, ensure_ascii=False)

        return {
            "success": True,
            "message": "Document analyzed and AI content generated successfully",
            "document_analysis_file": output_filename,
            "ai_output_file": final_output_filename,
            "data": ai_result,
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )

    finally:
        await file.close()

        if os.path.exists(input_path):
            os.remove(input_path)