from pydantic import BaseModel, Field, field_validator, field_serializer
from typing import Optional, List
from utils.roles import Roles
import datetime


class UserModel(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str

    roles: List[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value, info):
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value

    # 🔥 ВАЖНО: нормальная сериализация для API
    @field_serializer("roles")
    def serialize_roles(self, roles):
        return [role.value for role in roles]


class RegisterUserResponse(BaseModel):
    id: str
    email: str
    fullName: str
    verified: bool
    banned: bool
    roles: List[Roles]
    createdAt: str

    @field_validator("createdAt")
    def validate_created_at(cls, value):
        datetime.datetime.fromisoformat(value)
        return value