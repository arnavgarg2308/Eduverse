from pydantic import BaseModel


class QuizQuestion(BaseModel):

    question: str
    options: list[str]
    correct_answer: str


class QuizCreate(BaseModel):

    title: str
    questions: list[QuizQuestion]


class QuizSubmit(BaseModel):

    answers: list[str]