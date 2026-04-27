import pytest
from pydantic import ValidationError
from models.user_model import UserModel


def test_valid_user():
    data = {
        "email": "test@example.com",
        "fullName": "Ivan Ivanov",
        "password": "Test1234Aa",
        "passwordRepeat": "Test1234Aa",
        "roles": ["USER"]
    }

    user = UserModel(**data)

    assert user.email == data["email"]


def test_invalid_email():
    data = {
        "email": "invalid_email",  # ❌ нет @
        "fullName": "Ivan Ivanov",
        "password": "Test1234Aa",
        "roles": ["USER"]
    }

    with pytest.raises(ValidationError):
        UserModel(**data)


def test_invalid_password():
    data = {
        "email": "test@example.com",
        "fullName": "Ivan Ivanov",
        "password": "123",  # ❌ короткий
        "roles": ["USER"]
    }

    with pytest.raises(ValidationError):
        UserModel(**data)