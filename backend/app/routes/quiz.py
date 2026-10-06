from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId

from app.database.mongodb import database
from app.core.security import get_current_user, require_admin
from app.schemas.quiz import QuizCreate, QuizSubmit
from app.services.edumorph_service import generate_quiz_from_text


router = APIRouter(
    prefix="/api/quizzes",
    tags=["Quiz"],
)


# ============================================================
# CREATE QUIZ MANUALLY
# ============================================================

@router.post("/")
async def create_quiz(
    quiz: QuizCreate,
    current_user: dict = Depends(require_admin),
):
    new_quiz = quiz.model_dump()

    result = await database.quizzes.insert_one(
        new_quiz
    )

    return {
        "message": "Quiz created successfully",
        "quiz_id": str(result.inserted_id),
    }


# ============================================================
# GENERATE QUIZ FROM UPLOADED DOCUMENT
# ============================================================

@router.post("/generate/{document_id}")
async def generate_quiz(
    document_id: str,
    number_of_questions: int = 3,
    current_user: dict = Depends(get_current_user),
):
    # --------------------------------------------------------
    # Validate question count
    # --------------------------------------------------------

    if number_of_questions < 1:
        raise HTTPException(
            status_code=400,
            detail="number_of_questions must be at least 1.",
        )

    # --------------------------------------------------------
    # Validate document ID
    # --------------------------------------------------------

    try:
        document_object_id = ObjectId(
            document_id
        )

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid document ID.",
        )

    # --------------------------------------------------------
    # Get document belonging to current user
    # --------------------------------------------------------

    document = await database.documents.find_one(
        {
            "_id": document_object_id,
            "user_id": current_user["user_id"],
        }
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    # --------------------------------------------------------
    # Get extracted PDF text
    # --------------------------------------------------------

    extracted_text = document.get(
        "extracted_text",
        "",
    )

    if not extracted_text or not extracted_text.strip():
        raise HTTPException(
            status_code=400,
            detail=(
                "No extracted educational text is "
                "available for this document."
            ),
        )

    # --------------------------------------------------------
    # Determine education level
    # --------------------------------------------------------

    education_level = "General"

    analysis = document.get(
        "analysis",
        {},
    )

    if isinstance(analysis, dict):

        education_level = analysis.get(
            "education_level",
            "General",
        ) or "General"

    # --------------------------------------------------------
    # Generate quiz through AI Engine
    # --------------------------------------------------------

    try:

        ai_result = await generate_quiz_from_text(
            text=extracted_text,
            education_level=education_level,
            number_of_questions=number_of_questions,
        )

    except Exception as exc:

        print(
            f"[Quiz] AI generation error: {exc}"
        )

        raise HTTPException(
            status_code=502,
            detail=(
                "Quiz generation service is "
                "currently unavailable."
            ),
        )

    # --------------------------------------------------------
    # Extract questions from AI response
    # --------------------------------------------------------

    quiz_result = ai_result.get(
        "result",
        {},
    )

    if not isinstance(quiz_result, dict):
        raise HTTPException(
            status_code=502,
            detail="Invalid quiz response from AI Engine.",
        )

    questions = quiz_result.get(
        "questions",
        [],
    )

    if not isinstance(questions, list):
        raise HTTPException(
            status_code=502,
            detail="Invalid quiz questions from AI Engine.",
        )

    if not questions:
        raise HTTPException(
            status_code=422,
            detail=(
                "The uploaded document does not contain "
                "enough information to generate a meaningful quiz."
            ),
        )

    # --------------------------------------------------------
    # Clean and validate questions before saving
    # --------------------------------------------------------

    cleaned_questions = []

    for question in questions:

        if not isinstance(question, dict):
            continue

        question_text = str(
            question.get(
                "question",
                "",
            )
        ).strip()

        options = question.get(
            "options",
            [],
        )

        correct_answer = str(
            question.get(
                "correct_answer",
                "",
            )
        ).strip()

        explanation = str(
            question.get(
                "explanation",
                "",
            )
        ).strip()

        if not question_text:
            continue

        if not isinstance(options, list):
            continue

        if len(options) != 4:
            continue

        options = [
            str(option).strip()
            for option in options
        ]

        if any(
            not option
            for option in options
        ):
            continue

        if not correct_answer:
            continue

        if (
            correct_answer.lower()
            not in {
                option.lower()
                for option in options
            }
        ):
            continue

        cleaned_questions.append(
            {
                "question": question_text,
                "options": options,
                "correct_answer": correct_answer,
                "explanation": (
                    explanation
                    or "The uploaded material supports this answer."
                ),
            }
        )

    if not cleaned_questions:
        raise HTTPException(
            status_code=422,
            detail=(
                "The AI Engine did not return any "
                "valid quiz questions."
            ),
        )

    # --------------------------------------------------------
    # Quiz title
    # --------------------------------------------------------

    filename = document.get(
        "filename",
        "Uploaded Document",
    )

    title = (
        f"Quiz - {filename}"
    )

    # --------------------------------------------------------
    # Store generated quiz
    # --------------------------------------------------------

    quiz_document = {
        "user_id": current_user["user_id"],
        "document_id": document_id,
        "title": title,
        "education_level": education_level,
        "questions": cleaned_questions,
        "created_at": datetime.utcnow(),
        "source": "uploaded_document",
    }

    saved_quiz = await database.quizzes.insert_one(
        quiz_document
    )

    quiz_id = str(
        saved_quiz.inserted_id
    )

    # --------------------------------------------------------
    # Return quiz
    #
    # IMPORTANT:
    # correct_answer and explanation are returned here because
    # this endpoint is being used to create/load the quiz.
    # Later, the student-facing GET endpoint should hide the
    # correct answers until submission.
    # --------------------------------------------------------

    return {
        "message": "Quiz generated successfully",
        "quiz_id": quiz_id,
        "document_id": document_id,
        "title": title,
        "education_level": education_level,
        "questions": cleaned_questions,
        "generated_questions": len(
            cleaned_questions
        ),
        "requested_questions": number_of_questions,
    }


# ============================================================
# GET ALL QUIZZES
# ============================================================

@router.get("/")
async def get_all_quizzes():

    quizzes = []

    async for quiz in database.quizzes.find():

        quiz["quiz_id"] = str(
            quiz["_id"]
        )

        del quiz["_id"]

        quizzes.append(
            quiz
        )

    return quizzes


# ============================================================
# GET MY QUIZ RESULTS
# ============================================================

@router.get("/results/my-results")
async def get_my_quiz_results(
    current_user: dict = Depends(get_current_user),
):

    results = []

    async for result in database.quiz_results.find(
        {
            "user_id": current_user["user_id"]
        }
    ):

        result["result_id"] = str(
            result["_id"]
        )

        del result["_id"]

        results.append(
            result
        )

    return results


# ============================================================
# GET SINGLE QUIZ
# ============================================================

@router.get("/{quiz_id}")
async def get_quiz(
    quiz_id: str,
    current_user: dict = Depends(get_current_user),
):

    try:

        quiz = await database.quizzes.find_one(
            {
                "_id": ObjectId(quiz_id)
            }
        )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid quiz ID",
        )

    if not quiz:

        raise HTTPException(
            status_code=404,
            detail="Quiz not found",
        )

    # --------------------------------------------------------
    # Student should not receive correct answers before
    # submitting.
    # --------------------------------------------------------

    questions = []

    for question in quiz.get(
        "questions",
        [],
    ):

        questions.append(
            {
                "question": question[
                    "question"
                ],
                "options": question[
                    "options"
                ],
            }
        )

    return {
        "quiz_id": str(
            quiz["_id"]
        ),
        "title": quiz.get(
            "title"
        ),
        "questions": questions,
    }


# ============================================================
# SUBMIT QUIZ
# ============================================================

@router.post("/{quiz_id}/submit")
async def submit_quiz(
    quiz_id: str,
    answers: QuizSubmit,
    current_user: dict = Depends(get_current_user),
):

    try:

        quiz = await database.quizzes.find_one(
            {
                "_id": ObjectId(quiz_id)
            }
        )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid quiz ID",
        )

    if not quiz:

        raise HTTPException(
            status_code=404,
            detail="Quiz not found",
        )

    questions = quiz.get(
        "questions",
        [],
    )

    user_answers = answers.answers

    score = 0

    wrong_answers = []

    for index, question in enumerate(
        questions
    ):

        if index >= len(user_answers):

            wrong_answers.append(
                {
                    "question_number": index + 1,
                    "question": question[
                        "question"
                    ],
                    "user_answer": None,
                    "correct_answer": question[
                        "correct_answer"
                    ],
                    "explanation": question.get(
                        "explanation",
                        "",
                    ),
                }
            )

            continue

        user_answer = user_answers[
            index
        ]

        correct_answer = question[
            "correct_answer"
        ]

        if (
            user_answer.strip().lower()
            == correct_answer.strip().lower()
        ):

            score += 1

        else:

            wrong_answers.append(
                {
                    "question_number": index + 1,
                    "question": question[
                        "question"
                    ],
                    "user_answer": user_answer,
                    "correct_answer": correct_answer,
                    "explanation": question.get(
                        "explanation",
                        "",
                    ),
                }
            )

    total_questions = len(
        questions
    )

    percentage = (
        (score / total_questions) * 100
        if total_questions > 0
        else 0
    )

    result = {
        "user_id": current_user["user_id"],
        "quiz_id": quiz_id,
        "score": score,
        "total_questions": total_questions,
        "percentage": round(
            percentage,
            2,
        ),
        "wrong_answers": wrong_answers,
        "submitted_at": datetime.utcnow(),
    }

    saved_result = await database.quiz_results.insert_one(
        result
    )

    return {
        "message": "Quiz submitted successfully",
        "result_id": str(
            saved_result.inserted_id
        ),
        "user_id": current_user["user_id"],
        "quiz_id": quiz_id,
        "score": score,
        "total_questions": total_questions,
        "percentage": round(
            percentage,
            2,
        ),
        "wrong_answers": wrong_answers,
    }


# ============================================================
# DELETE QUIZ
# ============================================================

@router.delete("/{quiz_id}")
async def delete_quiz(
    quiz_id: str,
    current_user: dict = Depends(require_admin),
):

    try:

        result = await database.quizzes.delete_one(
            {
                "_id": ObjectId(quiz_id)
            }
        )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid quiz ID",
        )

    if result.deleted_count == 0:

        raise HTTPException(
            status_code=404,
            detail="Quiz not found",
        )

    return {
        "message": "Quiz deleted successfully"
    }