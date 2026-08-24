from fastapi import APIRouter, Depends

from app.database.mongodb import database
from app.core.security import get_current_user, require_admin


router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)


# Overall Dashboard - Admin Only
@router.get("/")
async def get_dashboard(
    current_user: dict = Depends(require_admin)
):

    total_users = await database.users.count_documents({})

    total_courses = await database.courses.count_documents({})

    total_documents = await database.documents.count_documents({})

    total_quizzes = await database.quizzes.count_documents({})

    total_lessons = await database.lessons.count_documents({})

    return {
        "total_users": total_users,
        "total_courses": total_courses,
        "total_documents": total_documents,
        "total_quizzes": total_quizzes,
        "total_lessons": total_lessons
    }

# Current User Dashboard
@router.get("/my-dashboard")
async def get_my_dashboard(
    current_user: dict = Depends(get_current_user)
):

    user_id = current_user["user_id"]

    # Total enrolled courses
    enrolled_courses = await database.enrollments.count_documents(
        {
            "user_id": user_id
        }
    )

    # Courses in progress
    courses_in_progress = await database.learning_progress.count_documents(
        {
            "user_id": user_id
        }
    )

    # Completed lessons
    completed_lessons = await database.lesson_completions.count_documents(
        {
            "user_id": user_id
        }
    )

    # Quiz attempts
    quiz_attempts = await database.quiz_results.count_documents(
        {
            "user_id": user_id
        }
    )

    # Calculate average quiz score
    results = []

    async for result in database.quiz_results.find(
        {
            "user_id": user_id
        }
    ):

        if result["total_questions"] > 0:

            percentage = (
                result["score"] /
                result["total_questions"]
            ) * 100

            results.append(percentage)

    average_quiz_score = 0

    if results:
        average_quiz_score = sum(results) / len(results)

    return {
        "user_id": user_id,
        "role": current_user.get("role"),
        "enrolled_courses": enrolled_courses,
        "courses_in_progress": courses_in_progress,
        "completed_lessons": completed_lessons,
        "quiz_attempts": quiz_attempts,
        "average_quiz_score": round(
            average_quiz_score,
            2
        )
    }