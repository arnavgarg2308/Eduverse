from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId

from app.database.mongodb import database
from app.core.security import require_admin
from app.schemas.lesson import LessonCreate, LessonUpdate


router = APIRouter(
    prefix="/api/lessons",
    tags=["Lessons"]
)


# Create Lesson - Admin Only
@router.post("/")
async def create_lesson(
    lesson: LessonCreate,
    current_user: dict = Depends(require_admin)
):

    course_id = lesson.course_id

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

    new_lesson = lesson.model_dump()

    result = await database.lessons.insert_one(
        new_lesson
    )

    return {
        "message": "Lesson created successfully",
        "lesson_id": str(result.inserted_id)
    }


# Get Lessons by Course - Anyone
@router.get("/course/{course_id}")
async def get_course_lessons(course_id: str):

    lessons = []

    async for lesson in database.lessons.find(
        {"course_id": course_id}
    ):

        lesson["lesson_id"] = str(lesson["_id"])
        del lesson["_id"]

        lessons.append(lesson)

    return lessons


# Get Single Lesson - Anyone
@router.get("/{lesson_id}")
async def get_lesson(lesson_id: str):

    try:
        lesson = await database.lessons.find_one(
            {"_id": ObjectId(lesson_id)}
        )

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid lesson ID"
        )

    if not lesson:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    lesson["lesson_id"] = str(lesson["_id"])
    del lesson["_id"]

    return lesson


# Update Lesson - Admin Only
@router.put("/{lesson_id}")
async def update_lesson(
    lesson_id: str,
    updated_data: LessonUpdate,
    current_user: dict = Depends(require_admin)
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
        result = await database.lessons.update_one(
            {"_id": ObjectId(lesson_id)},
            {"$set": update_data}
        )

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid lesson ID"
        )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    return {
        "message": "Lesson updated successfully"
    }


# Delete Lesson - Admin Only
@router.delete("/{lesson_id}")
async def delete_lesson(
    lesson_id: str,
    current_user: dict = Depends(require_admin)
):

    try:
        result = await database.lessons.delete_one(
            {"_id": ObjectId(lesson_id)}
        )

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid lesson ID"
        )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    return {
        "message": "Lesson deleted successfully"
    }