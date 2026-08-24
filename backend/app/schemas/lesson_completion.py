from pydantic import BaseModel


class LessonCompletionCreate(BaseModel):
    course_id: str
    lesson_id: str


class LessonCompletionUpdate(BaseModel):
    status: str | None = None