from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserProfileUpdate(BaseModel):

    name: str | None = None

    email: EmailStr | None = None

class ChangePassword(BaseModel):

    current_password: str

    new_password: str