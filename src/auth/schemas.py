from pydantic import BaseModel, ConfigDict


class BaseUser(BaseModel):
    username: str


class UserCreate(BaseUser):
    username: str
    name: str
    password: str


class UserAuth(BaseUser):
    id: int
    username: str
    name: str
    hashed_password: str


class User(BaseUser):
    id: int
    username: str
    name: str
