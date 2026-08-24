from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId

from app.database.mongodb import database
from app.core.security import get_current_user
from app.schemas.learning import LearningProgressCreate, LearningProgressUpdate


router = APIRouter(
    prefix="/api/learning",
    tags=["Learning"]
)


# Add Learning Progress
@router.post("/progress")
async def add_learning_progress(
    progress: LearningProgressCreate,
    current_user: dict = Depends(get_current_user)
):

    progress_data = progress.model_dump()

    course_id = progress_data.get("course_id")
    lesson_id = progress_data.get("lesson_id")

    # Check Course
    try:
        course = await database.courses.find_one(
            {"_id": ObjectId(course_id)}
        )

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid course ID"
        )

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    # Check Lesson if lesson_id is provided
    if lesson_id:

        try:
            lesson = await database.lessons.find_one(
                {
                    "_id": ObjectId(lesson_id),
                    "course_id": course_id
                }
            )

        except:
            raise HTTPException(
                status_code=400,
                detail="Invalid lesson ID"
            )

        if not lesson:
            raise HTTPException(
                status_code=404,
                detail="Lesson not found for this course"
            )

    progress_data["user_id"] = current_user["user_id"]

    # Prevent duplicate progress
    existing_progress = await database.learning_progress.find_one(
        {
            "user_id": current_user["user_id"],
            "course_id": course_id,
            "lesson_id": lesson_id
        }
    )

    if existing_progress:
        raise HTTPException(
            status_code=400,
            detail="Learning progress already exists"
        )

    result = await database.learning_progress.insert_one(
        progress_data
    )

    return {
        "message": "Learning progress added successfully",
        "progress_id": str(result.inserted_id),
        "user_id": current_user["user_id"],
        "course_id": course_id,
        "lesson_id": lesson_id
    }


# Get Current User Progress
@router.get("/progress")
async def get_my_progress(
    current_user: dict = Depends(get_current_user)
):

    progress_list = []

    async for progress in database.learning_progress.find(
        {"user_id": current_user["user_id"]}
    ):

        progress["progress_id"] = str(progress["_id"])
        del progress["_id"]

        progress_list.append(progress)

    return progress_list


# Get Single Progress
@router.get("/progress/{progress_id}")
async def get_progress(
    progress_id: str,
    current_user: dict = Depends(get_current_user)
):

    try:
        progress = await database.learning_progress.find_one(
            {
                "_id": ObjectId(progress_id),
                "user_id": current_user["user_id"]
            }
        )

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid progress ID"
        )

    if not progress:
        raise HTTPException(
            status_code=404,
            detail="Progress not found"
        )

    progress["progress_id"] = str(progress["_id"])
    del progress["_id"]

    return progress


# Update Progress
@router.put("/progress/{progress_id}")
async def update_progress(
    progress_id: str,
    updated_data: LearningProgressUpdate,
    current_user: dict = Depends(get_current_user)
):

    update_data = updated_data.model_dump(
        exclude_none=True
    )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No data provided for update"
        )

    try:
        result = await database.learning_progress.update_one(
            {
                "_id": ObjectId(progress_id),
                "user_id": current_user["user_id"]
            },
            {
                "$set": update_data
            }
        )

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid progress ID"
        )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Progress not found"
        )

    return {
        "message": "Learning progress updated successfully"
    }


# Delete Progress
@router.delete("/progress/{progress_id}")
async def delete_progress(
    progress_id: str,
    current_user: dict = Depends(get_current_user)
):

    try:
        result = await database.learning_progress.delete_one(
            {
                "_id": ObjectId(progress_id),
                "user_id": current_user["user_id"]
            }
        )

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid progress ID"
        )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Progress not found"
        )

    return {
        "message": "Learning progress deleted successfully"
    }