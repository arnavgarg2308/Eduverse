from pydantic import BaseModel


class LessonCreate(BaseModel):

    course_id: str
    title: str
    content: str


class LessonUpdate(BaseModel):

    title: str | None = None
    content: str | None = None