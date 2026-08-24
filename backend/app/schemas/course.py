from pydantic import BaseModel


class CourseCreate(BaseModel):

    title: str

    description: str

    category: str

    level: str

class CourseUpdate(BaseModel):

    title: str | None = None

    description: str | None = None

    category: str | None = None

    level: str | None = None