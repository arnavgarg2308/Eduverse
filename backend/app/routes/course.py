from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId

from app.schemas.course import CourseCreate, CourseUpdate
from app.database.mongodb import database
from app.core.security import require_admin


router = APIRouter(
    prefix="/api/courses",
    tags=["Courses"]
)


# Create Course - Admin Only
@router.post("/")
async def create_course(
    course: CourseCreate,
    current_user: dict = Depends(require_admin)
):

    new_course = {
        "title": course.title,
        "description": course.description,
        "category": course.category,
        "level": course.level
    }

    result = await database.courses.insert_one(
        new_course
    )

    return {
        "message": "Course created successfully",
        "course_id": str(result.inserted_id),
        "title": course.title
    }


# Get All Courses - Anyone
@router.get("/")
async def get_all_courses():

    courses = []

    async for course in database.courses.find():

        courses.append({
            "course_id": str(course["_id"]),
            "title": course["title"],
            "description": course["description"],
            "category": course["category"],
            "level": course["level"]
        })

    return courses


# Get Single Course - Anyone
@router.get("/{course_id}")
async def get_course(course_id: str):

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

    return {
        "course_id": str(course["_id"]),
        "title": course["title"],
        "description": course["description"],
        "category": course["category"],
        "level": course["level"]
    }


# Update Course - Admin Only
@router.put("/{course_id}")
async def update_course(
    course_id: str,
    course: CourseUpdate,
    current_user: dict = Depends(require_admin)
):

    try:
        object_id = ObjectId(course_id)

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid course ID"
        )

    update_data = course.model_dump(
        exclude_none=True
    )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No data provided for update"
        )

    result = await database.courses.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    updated_course = await database.courses.find_one(
        {"_id": object_id}
    )

    return {
        "message": "Course updated successfully",
        "course_id": str(updated_course["_id"]),
        "title": updated_course["title"],
        "description": updated_course["description"],
        "category": updated_course["category"],
        "level": updated_course["level"]
    }


# Delete Course - Admin Only
@router.delete("/{course_id}")
async def delete_course(
    course_id: str,
    current_user: dict = Depends(require_admin)
):

    try:
        result = await database.courses.delete_one(
            {"_id": ObjectId(course_id)}
        )

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid course ID"
        )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return {
        "message": "Course deleted successfully",
        "course_id": course_id
    }