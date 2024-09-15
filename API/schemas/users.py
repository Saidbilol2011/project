from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    username: str
    role: str


class UserCreateSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    phone: str
    role: str
    gender: str


class UserLoginSchema(BaseModel):
    username: str
    password: str