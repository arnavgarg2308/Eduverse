import os
import shutil
import uuid

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from src.pipeline.document_analyzer import DocumentAnalyzer


app = FastAPI(
    title="EduMorph Document Intelligence API",
    description="API for analyzing educational PDF documents",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_DIRECTORY = "uploads"
OUTPUT_DIRECTORY = "outputs"


os.makedirs(
    UPLOAD_DIRECTORY,
    exist_ok=True
)


os.makedirs(
    OUTPUT_DIRECTORY,
    exist_ok=True
)


@app.get("/")
def home():

    return {
        "message": "EduMorph Document Intelligence API is running"
    }


@app.post("/analyze")
async def analyze_pdf(
    file: UploadFile = File(...)
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file was uploaded"
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    file_id = str(
        uuid.uuid4()
    )

    input_filename = (
        f"{file_id}_{file.filename}"
    )

    input_path = os.path.join(
        UPLOAD_DIRECTORY,
        input_filename
    )

    original_name = os.path.splitext(
        file.filename
    )[0]

    output_filename = (
        f"{original_name}_analysis.json"
    )

    output_path = os.path.join(
        OUTPUT_DIRECTORY,
        output_filename
    )

    try:

        with open(
            input_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        analyzer = DocumentAnalyzer()

        analyzer.analyze(
            input_path,
            output_path
        )

        return FileResponse(
            path=output_path,
            media_type="application/json",
            filename=output_filename
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    finally:

        await file.close()

        if os.path.exists(
            input_path
        ):

            os.remove(
                input_path
            )
