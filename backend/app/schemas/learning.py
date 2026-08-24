from pydantic import BaseModel


class LearningProgressCreate(BaseModel):

    course_id: str
    lesson_id: str | None = None
    status: str = "in_progress"


class LearningProgressUpdate(BaseModel):

    status: str | None = None