from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from datetime import datetime
from pathlib import Path
from fastapi.responses import StreamingResponse
from io import BytesIO

from app.database.mongodb import database, gridfs_bucket
from app.core.security import get_current_user
from app.services.video_service import generate_video_from_text


router = APIRouter(
    prefix="/api/videos",
    tags=["Videos"]
)


# ==========================================
# Generate Video from Uploaded PDF
# ==========================================

@router.post("/generate/{document_id}")
async def generate_video(
    document_id: str,
    current_user: dict = Depends(get_current_user)
):

    # Get document
    try:
        document = await database.documents.find_one(
            {
                "_id": ObjectId(document_id),
                "user_id": current_user["user_id"]
            }
        )

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid document ID"
        )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # Get extracted text
    extracted_text = document.get("extracted_text", "")

    if not extracted_text:
        raise HTTPException(
            status_code=400,
            detail="No text found in this PDF"
        )

    # Temporary video path
    output_path = f"temp_videos/{document_id}.mp4"

    # Generate video
    try:
        generate_video_from_text(
            extracted_text,
            output_path
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    # Read generated video
    try:
        with open(output_path, "rb") as video_file:
            video_data = video_file.read()

    except:
        raise HTTPException(
            status_code=500,
            detail="Generated video file not found"
        )

    # Store video in GridFS
    video_file_id = await gridfs_bucket.upload_from_stream(
        f"{document_id}.mp4",
        video_data,
        metadata={
            "user_id": current_user["user_id"],
            "document_id": document_id,
            "content_type": "video/mp4",
            "generated_at": datetime.utcnow()
        }
    )

    # Save video metadata
    video_data_db = {
        "user_id": current_user["user_id"],
        "document_id": document_id,
        "video_file_id": str(video_file_id),
        "filename": f"{document_id}.mp4",
        "status": "generated",
        "generated_at": datetime.utcnow()
    }

    result = await database.videos.insert_one(
        video_data_db
    )

    # Remove temporary video
    Path(output_path).unlink(missing_ok=True)

    return {
        "message": "Video generated successfully",
        "video_id": str(result.inserted_id),
        "video_file_id": str(video_file_id),
        "document_id": document_id,
        "status": "generated"
    }
# ==========================================
# Stream Generated Video
# ==========================================

@router.get("/stream/{video_id}")
async def stream_video(
    video_id: str,
    current_user: dict = Depends(get_current_user)
):

    try:
        video = await database.videos.find_one(
            {
                "_id": ObjectId(video_id),
                "user_id": current_user["user_id"]
            }
        )

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid video ID"
        )

    if not video:
        raise HTTPException(
            status_code=404,
            detail="Video not found"
        )

    try:
        grid_out = await gridfs_bucket.open_download_stream(
            ObjectId(video["video_file_id"])
        )

        video_data = await grid_out.read()

    except:
        raise HTTPException(
            status_code=500,
            detail="Failed to load video"
        )

    return StreamingResponse(
        BytesIO(video_data),
        media_type="video/mp4"
    )

# ==========================================
# Get Video Details
# ==========================================

@router.get("/{video_id}")
async def get_video(
    video_id: str,
    current_user: dict = Depends(get_current_user)
):

    try:
        video = await database.videos.find_one(
            {
                "_id": ObjectId(video_id),
                "user_id": current_user["user_id"]
            }
        )

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid video ID"
        )

    if not video:
        raise HTTPException(
            status_code=404,
            detail="Video not found"
        )

    video["video_id"] = str(video["_id"])
    del video["_id"]

    return video