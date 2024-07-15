from pydantic import BaseModel, ConfigDict
from datetime import datetime


class UserInDB(BaseModel):
    id: int
    username: str
    name: str
    hashed_password: str
    created_date: datetime


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


class Token(BaseModel):
    access_token: str
    token_type: str
