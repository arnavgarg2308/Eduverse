from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId

from app.database.mongodb import database
from app.core.security import get_current_user, require_admin
from app.schemas.quiz import QuizCreate, QuizSubmit


router = APIRouter(
    prefix="/api/quizzes",
    tags=["Quiz"]
)


# Create Quiz - Admin Only
@router.post("/")
async def create_quiz(
    quiz: QuizCreate,
    current_user: dict = Depends(require_admin)
):

    new_quiz = quiz.model_dump()

    result = await database.quizzes.insert_one(
        new_quiz
    )

    return {
        "message": "Quiz created successfully",
        "quiz_id": str(result.inserted_id)
    }


# Get All Quizzes - Anyone
@router.get("/")
async def get_all_quizzes():

    quizzes = []

    async for quiz in database.quizzes.find():

        quiz["quiz_id"] = str(quiz["_id"])
        del quiz["_id"]

        quizzes.append(quiz)

    return quizzes


# Get Current User Quiz Results
# This must come before /{quiz_id}
@router.get("/results/my-results")
async def get_my_quiz_results(
    current_user: dict = Depends(get_current_user)
):

    results = []

    async for result in database.quiz_results.find(
        {"user_id": current_user["user_id"]}
    ):

        result["result_id"] = str(result["_id"])
        del result["_id"]

        results.append(result)

    return results


# Get Single Quiz - Anyone
@router.get("/{quiz_id}")
async def get_quiz(quiz_id: str):

    try:
        quiz = await database.quizzes.find_one(
            {"_id": ObjectId(quiz_id)}
        )

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid quiz ID"
        )

    if not quiz:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found"
        )

    questions = []

    for question in quiz["questions"]:

        questions.append({
            "question": question["question"],
            "options": question["options"]
        })

    return {
        "quiz_id": str(quiz["_id"]),
        "title": quiz.get("title"),
        "questions": questions
    }


# Submit Quiz - Logged-in User
@router.post("/{quiz_id}/submit")
async def submit_quiz(
    quiz_id: str,
    answers: QuizSubmit,
    current_user: dict = Depends(get_current_user)
):

    try:
        quiz = await database.quizzes.find_one(
            {"_id": ObjectId(quiz_id)}
        )

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid quiz ID"
        )

    if not quiz:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found"
        )

    score = 0

    user_answers = answers.answers

    for index, question in enumerate(quiz["questions"]):

        if index < len(user_answers):

            if user_answers[index] == question["correct_answer"]:
                score += 1

    result = {
        "user_id": current_user["user_id"],
        "quiz_id": quiz_id,
        "score": score,
        "total_questions": len(quiz["questions"])
    }

    saved_result = await database.quiz_results.insert_one(
        result
    )

    return {
        "message": "Quiz submitted successfully",
        "result_id": str(saved_result.inserted_id),
        "user_id": current_user["user_id"],
        "quiz_id": quiz_id,
        "score": score,
        "total_questions": len(quiz["questions"])
    }


# Delete Quiz - Admin Only
@router.delete("/{quiz_id}")
async def delete_quiz(
    quiz_id: str,
    current_user: dict = Depends(require_admin)
):

    try:
        result = await database.quizzes.delete_one(
            {"_id": ObjectId(quiz_id)}
        )

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid quiz ID"
        )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found"
        )

    return {
        "message": "Quiz deleted successfully"
    }