import json
import os
import shutil
import uuid
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from src.pipeline.document_analyzer import DocumentAnalyzer

from app.routes.auth import router as auth_router
from app.routes.course import router as course_router


# ============================================================
# OTHER SERVICES
# ============================================================

AI_ENGINE_URL = "http://127.0.0.1:8002/process-document"
VIDEO_ENGINE_URL = "http://127.0.0.1:8003/generate-video"


# ============================================================
# ADAPTER
# AI ENGINE OUTPUT -> MEDIA PIPELINE SCENE PLAN
# ============================================================

def convert_to_scene_plan(ai_output: dict) -> dict:
    """
    AI Engine ke output ko Media Generation Pipeline ke
    required scene_plan format mein convert karta hai.
    """

    # AI engine ka actual generated result
    result = ai_output.get("result", ai_output)

    # --------------------------------------------------------
    # CASE 1: AI already gives scenes
    # --------------------------------------------------------

    if isinstance(result, dict) and isinstance(result.get("scenes"), list):

        formatted_scenes = []

        for index, scene in enumerate(result["scenes"], start=1):

            if not isinstance(scene, dict):
                continue

            formatted_scenes.append({
                "scene_number": scene.get("scene_number", index),
                "title": scene.get("title", f"Scene {index}"),
                "narration": (
                    scene.get("narration")
                    or scene.get("script")
                    or scene.get("content")
                    or scene.get("text")
                    or ""
                ),
                "visual_description": (
                    scene.get("visual_description")
                    or scene.get("visual")
                    or scene.get("description")
                    or scene.get("narration")
                    or ""
                )
            })

        if formatted_scenes:
            return {"scenes": formatted_scenes}

    # --------------------------------------------------------
    # CASE 2: AI result is a string
    # --------------------------------------------------------

    if isinstance(result, str):
        narration = result

    # --------------------------------------------------------
    # CASE 3: Use extracted PDF content as fallback
    # --------------------------------------------------------

    else:
        narration = ai_output.get(
            "extracted_content",
            ""
        )

        if not narration and isinstance(result, dict):
            narration = (
                result.get("summary")
                or result.get("content")
                or result.get("script")
                or result.get("explanation")
                or ""
            )

    narration = str(narration).strip()

    if not narration:
        raise ValueError(
            "Could not create narration from AI Engine output."
        )

    return {
        "scenes": [
            {
                "scene_number": 1,
                "title": ai_output.get(
                    "topic",
                    "Educational Lesson"
                ),
                "narration": narration,
                "visual_description": (
                    "Create an educational animated visualization "
                    "that explains the narration clearly."
                )
            }
        ]
    }


# ============================================================
# APP LIFESPAN
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    yield


app = FastAPI(
    title="AI Learning Platform API",
    version="1.0.0",
    lifespan=lifespan
)


# ============================================================
# CORS
# ============================================================

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


# ============================================================
# FOLDERS
# ============================================================

UPLOAD_DIRECTORY = "uploads"
OUTPUT_DIRECTORY = "output"

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)


# ============================================================
# ROUTES
# ============================================================

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


# ============================================================
# EDUVERSE PDF -> AI -> VIDEO
# ============================================================

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
    input_path = os.path.join(
        UPLOAD_DIRECTORY,
        input_filename
    )

    original_name = os.path.splitext(file.filename)[0]

    output_filename = f"{original_name}_analysis.json"
    output_path = os.path.join(
        OUTPUT_DIRECTORY,
        output_filename
    )

    final_output_filename = (
        f"{original_name}_ai_output.json"
    )

    final_output_path = os.path.join(
        OUTPUT_DIRECTORY,
        final_output_filename
    )

    try:

        # ====================================================
        # 1. SAVE PDF
        # ====================================================

        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        print("\n[STEP 1] PDF saved successfully")


        # ====================================================
        # 2. ANALYZE PDF
        # ====================================================

        analyzer = DocumentAnalyzer()

        analyzer.analyze(
            input_path,
            output_path
        )

        with open(
            output_path,
            "r",
            encoding="utf-8"
        ) as json_file:

            document_json = json.load(json_file)

        print("[STEP 2] PDF analyzed successfully")


        # ====================================================
        # 3. SEND TO AI ENGINE (8002)
        # ====================================================

        print("[STEP 3] Sending document to AI Engine...")

        async with httpx.AsyncClient(
            timeout=600.0
        ) as client:

            response = await client.post(
                AI_ENGINE_URL,
                json={
                    "document": document_json,
                    "topic": "General",
                    "education_level": "Grade 9",
                    "number_of_questions": 3,
                },
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=500,
                    detail=(
                        f"AI Engine Error: "
                        f"{response.text}"
                    ),
                )

            ai_result = response.json()

            print("[STEP 3] AI content generated successfully")


            # ====================================================
            # 4. ADAPTER -> CREATE SCENE PLAN
            # ====================================================

            print("[STEP 4] Converting AI output to scene plan...")

            scene_plan = convert_to_scene_plan(
                ai_result
            )

            print(
                f"Created {len(scene_plan['scenes'])} scene(s)"
            )


            # ====================================================
            # 5. SEND TO VIDEO ENGINE (8003)
            # ====================================================

            print("[STEP 5] Starting video generation...")

            video_response = await client.post(
                VIDEO_ENGINE_URL,
                json={
                    "scene_plan": scene_plan
                },
                timeout=600.0,
            )

        if video_response.status_code != 200:

            raise HTTPException(
                status_code=500,
                detail=(
                    f"Video Engine Error: "
                    f"{video_response.text}"
                ),
            )

        video_result = video_response.json()

        print("[STEP 5] VIDEO GENERATED SUCCESSFULLY!")


        # ====================================================
        # 6. SAVE AI OUTPUT
        # ====================================================

        with open(
            final_output_path,
            "w",
            encoding="utf-8"
        ) as final_file:

            json.dump(
                ai_result,
                final_file,
                indent=4,
                ensure_ascii=False
            )


        # ====================================================
        # FINAL RESPONSE -> FRONTEND
        # ====================================================

        return {
    "success": True,
    "message": "Document analyzed and video generated successfully",
    "document_analysis_file": output_filename,
    "ai_output_file": final_output_filename,
    "data": ai_result,
    "video": video_result
}


    except HTTPException:
        raise

    except Exception as error:

        print(f"\nERROR: {str(error)}")

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )

    finally:

        await file.close()

        if os.path.exists(input_path):
            os.remove(input_path)