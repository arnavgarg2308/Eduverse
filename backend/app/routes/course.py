from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.schemas.course import CourseCreate
from app.database.mongodb import database


router = APIRouter(
    prefix="/api/courses",
    tags=["Courses"]
)


@router.post("/")
async def create_course(course: CourseCreate):

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