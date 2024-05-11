from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: int
    avatar: str
    updated_at: datetime


class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr
    avatar: str
    role: int
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]
