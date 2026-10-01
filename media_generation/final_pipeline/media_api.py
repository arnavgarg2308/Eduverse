from fastapi import FastAPI, HTTPException
from pathlib import Path
import subprocess
import sys
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="EduVerse Media Generation API",
    version="1.0.0"
)

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "outputs"
FINAL_VIDEO = OUTPUT_DIR / "final_educational_video.mp4"

PIPELINE_FILE = BASE_DIR / "auto_pipeline.py"

OUTPUT_DIR.mkdir(exist_ok=True)

# Final generated videos serve karne ke liye
app.mount(
    "/videos",
    StaticFiles(directory=str(OUTPUT_DIR)),
    name="videos"
)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "EduVerse Media Generation"
    }


# ============================================================
# GENERATE VIDEO
# ============================================================

@app.post("/generate-video")
def generate_video():

    try:

        print("\n====================================")
        print("STARTING VIDEO GENERATION")
        print("Using latest scene plan JSON...")
        print("====================================\n")

        # Purana final video remove karo
        if FINAL_VIDEO.exists():
            FINAL_VIDEO.unlink()

        # auto_pipeline.py latest scene_plan.json ko read karega
        subprocess.run(
            [
                sys.executable,
                str(PIPELINE_FILE)
            ],
            cwd=str(BASE_DIR),
            check=True
        )

        # Check final video
        if not FINAL_VIDEO.exists():
            raise RuntimeError(
                "Pipeline completed but final video was not found."
            )

        return {
    "success": True,
    "message": "Video generated successfully",
    "filename": FINAL_VIDEO.name,
    "video_url": f"http://127.0.0.1:8003/videos/{FINAL_VIDEO.name}?v={int(FINAL_VIDEO.stat().st_mtime)}"
}

    except subprocess.CalledProcessError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Media pipeline failed: {str(exc)}"
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )