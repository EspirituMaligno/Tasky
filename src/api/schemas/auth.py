from datetime import date, datetime

from pydantic import BaseModel


class AuthResponseModel(BaseModel):
    status: str
    message: str


class TokenDataSchema(BaseModel):
    access_token: str
    refresh_token: str


class UserCreateSchema(BaseModel):
    name: str
    surname: str
    date_of_birth: date
    username: str
    password: str


class UserLoginSchema(BaseModel):
    username: str
    password: str
