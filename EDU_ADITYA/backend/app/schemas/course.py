from pydantic import BaseModel


class CourseCreate(BaseModel):

    title: str

    description: str

    category: str

    level: str