from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId

from app.database.mongodb import database
from app.core.security import get_current_user
from app.schemas.lesson_completion import (
    LessonCompletionCreate,
    LessonCompletionUpdate
)


router = APIRouter(
    prefix="/api/lesson-completions",
    tags=["Lesson Completions"]
)


# Mark Lesson as Completed
@router.post("/")
async def complete_lesson(
    completion: LessonCompletionCreate,
    current_user: dict = Depends(get_current_user)
):

    data = completion.model_dump()

    course_id = data["course_id"]
    lesson_id = data["lesson_id"]

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

    # Check Enrollment
    enrollment = await database.enrollments.find_one(
        {
            "user_id": current_user["user_id"],
            "course_id": course_id
        }
    )

    if not enrollment:
        raise HTTPException(
            status_code=400,
            detail="You must enroll in this course first"
        )

    # Check Lesson
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

    # Prevent duplicate completion
    existing_completion = await database.lesson_completions.find_one(
        {
            "user_id": current_user["user_id"],
            "course_id": course_id,
            "lesson_id": lesson_id
        }
    )

    if existing_completion:
        raise HTTPException(
            status_code=400,
            detail="Lesson already completed"
        )

    # Save completion
    completion_data = {
        "user_id": current_user["user_id"],
        "course_id": course_id,
        "lesson_id": lesson_id,
        "status": "completed"
    }

    result = await database.lesson_completions.insert_one(
        completion_data
    )

    # Count total lessons in course
    total_lessons = await database.lessons.count_documents(
        {
            "course_id": course_id
        }
    )

    # Count completed lessons by current user
    completed_lessons = await database.lesson_completions.count_documents(
        {
            "user_id": current_user["user_id"],
            "course_id": course_id,
            "status": "completed"
        }
    )

    # Calculate progress percentage
    progress = 0

    if total_lessons > 0:
        progress = round(
            (completed_lessons / total_lessons) * 100,
            2
        )

    # Update enrollment status
    enrollment_status = "active"

    if progress == 100:
        enrollment_status = "completed"

    await database.enrollments.update_one(
        {
            "user_id": current_user["user_id"],
            "course_id": course_id
        },
        {
            "$set": {
                "progress": progress,
                "status": enrollment_status
            }
        }
    )

    return {
        "message": "Lesson marked as completed",
        "completion_id": str(result.inserted_id),
        "course_id": course_id,
        "lesson_id": lesson_id,
        "completed_lessons": completed_lessons,
        "total_lessons": total_lessons,
        "progress": progress,
        "course_status": enrollment_status
    }


# Get My Completed Lessons
@router.get("/")
async def get_my_completed_lessons(
    current_user: dict = Depends(get_current_user)
):

    completions = []

    async for completion in database.lesson_completions.find(
        {
            "user_id": current_user["user_id"]
        }
    ):

        completion["completion_id"] = str(
            completion["_id"]
        )

        del completion["_id"]

        completions.append(completion)

    return completions


# Get Single Completion
@router.get("/{completion_id}")
async def get_completion(
    completion_id: str,
    current_user: dict = Depends(get_current_user)
):

    try:
        completion = await database.lesson_completions.find_one(
            {
                "_id": ObjectId(completion_id),
                "user_id": current_user["user_id"]
            }
        )

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid completion ID"
        )

    if not completion:
        raise HTTPException(
            status_code=404,
            detail="Lesson completion not found"
        )

    completion["completion_id"] = str(
        completion["_id"]
    )

    del completion["_id"]

    return completion


# Update Completion Status
# Update Completion Status
@router.put("/{completion_id}")
async def update_completion(
    completion_id: str,
    updated_data: LessonCompletionUpdate,
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
        completion = await database.lesson_completions.find_one(
            {
                "_id": ObjectId(completion_id),
                "user_id": current_user["user_id"]
            }
        )

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid completion ID"
        )

    if not completion:
        raise HTTPException(
            status_code=404,
            detail="Lesson completion not found"
        )

    await database.lesson_completions.update_one(
        {
            "_id": ObjectId(completion_id)
        },
        {
            "$set": update_data
        }
    )

    course_id = completion["course_id"]

    # Count total lessons
    total_lessons = await database.lessons.count_documents(
        {
            "course_id": course_id
        }
    )

    # Count completed lessons
    completed_lessons = await database.lesson_completions.count_documents(
        {
            "user_id": current_user["user_id"],
            "course_id": course_id,
            "status": "completed"
        }
    )

    progress = 0

    if total_lessons > 0:
        progress = round(
            (completed_lessons / total_lessons) * 100,
            2
        )

    enrollment_status = "active"

    if progress == 100:
        enrollment_status = "completed"

    # Update enrollment progress
    await database.enrollments.update_one(
        {
            "user_id": current_user["user_id"],
            "course_id": course_id
        },
        {
            "$set": {
                "progress": progress,
                "status": enrollment_status
            }
        }
    )

    return {
        "message": "Lesson completion updated successfully",
        "progress": progress,
        "course_status": enrollment_status
    }

# Delete Completion
@router.delete("/{completion_id}")
async def delete_completion(
    completion_id: str,
    current_user: dict = Depends(get_current_user)
):

    try:
        completion = await database.lesson_completions.find_one(
            {
                "_id": ObjectId(completion_id),
                "user_id": current_user["user_id"]
            }
        )

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid completion ID"
        )

    if not completion:
        raise HTTPException(
            status_code=404,
            detail="Lesson completion not found"
        )

    course_id = completion["course_id"]

    # Delete completion
    await database.lesson_completions.delete_one(
        {
            "_id": ObjectId(completion_id),
            "user_id": current_user["user_id"]
        }
    )

    # Count total lessons
    total_lessons = await database.lessons.count_documents(
        {
            "course_id": course_id
        }
    )

    # Count remaining completed lessons
    completed_lessons = await database.lesson_completions.count_documents(
        {
            "user_id": current_user["user_id"],
            "course_id": course_id,
            "status": "completed"
        }
    )

    progress = 0

    if total_lessons > 0:
        progress = round(
            (completed_lessons / total_lessons) * 100,
            2
        )

    enrollment_status = "active"

    if progress == 100:
        enrollment_status = "completed"

    # Update enrollment
    await database.enrollments.update_one(
        {
            "user_id": current_user["user_id"],
            "course_id": course_id
        },
        {
            "$set": {
                "progress": progress,
                "status": enrollment_status
            }
        }
    )

    return {
        "message": "Lesson completion deleted successfully",
        "progress": progress,
        "course_status": enrollment_status
    }