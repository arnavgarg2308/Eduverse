from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId

from app.database.mongodb import database
from app.core.security import get_current_user


router = APIRouter(
    prefix="/api/enrollments",
    tags=["Enrollments"]
)


# Enroll in a course
@router.post("/{course_id}")
async def enroll_in_course(
    course_id: str,
    current_user: dict = Depends(get_current_user)
):

    try:
        course_object_id = ObjectId(course_id)

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid course ID"
        )

    course = await database.courses.find_one(
        {"_id": course_object_id}
    )

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    existing_enrollment = await database.enrollments.find_one(
        {
            "user_id": current_user["user_id"],
            "course_id": course_id
        }
    )

    if existing_enrollment:
        raise HTTPException(
            status_code=400,
            detail="Already enrolled in this course"
        )

    enrollment = {
        "user_id": current_user["user_id"],
        "course_id": course_id,
        "progress": 0,
        "status": "active"
    }

    result = await database.enrollments.insert_one(
        enrollment
    )

    return {
        "message": "Enrolled successfully",
        "enrollment_id": str(result.inserted_id),
        "course_id": course_id
    }


# Get My Enrollments
@router.get("/")
async def get_my_enrollments(
    current_user: dict = Depends(get_current_user)
):

    enrollments = []

    async for enrollment in database.enrollments.find(
        {
            "user_id": current_user["user_id"]
        }
    ):

        enrollment["enrollment_id"] = str(
            enrollment["_id"]
        )

        del enrollment["_id"]

        enrollments.append(enrollment)

    return enrollments


# Unenroll from a Course
@router.delete("/{course_id}")
async def unenroll_from_course(
    course_id: str,
    current_user: dict = Depends(get_current_user)
):

    result = await database.enrollments.delete_one(
        {
            "user_id": current_user["user_id"],
            "course_id": course_id
        }
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    return {
        "message": "Unenrolled successfully"
    }