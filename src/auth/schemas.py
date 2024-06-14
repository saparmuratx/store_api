from pydantic import BaseModel, ConfigDict
from datetime import datetime


class UserAuth(BaseModel):
    id: int
    username: str
    name: str
    hashed_password: str


class BaseUser(BaseModel):
    username: str
    name: str


class UserCreate(BaseUser):
    password: str


class User(BaseUser):
    id: int
    created_date: datetime


class UserUpdate(BaseUser):
    pass


class UserChangePassword(BaseModel):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str
