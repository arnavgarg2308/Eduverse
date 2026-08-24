from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId

from app.database.mongodb import database
from app.core.security import get_current_user


router = APIRouter(
    prefix="/api/course-progress",
    tags=["Course Progress"]
)


# Get progress of current user for a course
@router.get("/{course_id}")
async def get_course_progress(
    course_id: str,
    current_user: dict = Depends(get_current_user)
):

    try:
        course = await database.courses.find_one(
            {
                "_id": ObjectId(course_id)
            }
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

    # Total lessons in the course
    total_lessons = await database.lessons.count_documents(
        {
            "course_id": course_id
        }
    )

    # Completed lessons by current user
    completed_lessons = await database.lesson_completions.count_documents(
        {
            "user_id": current_user["user_id"],
            "course_id": course_id
        }
    )

    # Calculate percentage
    if total_lessons == 0:
        progress_percentage = 0
    else:
        progress_percentage = round(
            (completed_lessons / total_lessons) * 100,
            2
        )

    return {
        "course_id": course_id,
        "course_title": course.get("title"),
        "total_lessons": total_lessons,
        "completed_lessons": completed_lessons,
        "progress_percentage": progress_percentage
    }