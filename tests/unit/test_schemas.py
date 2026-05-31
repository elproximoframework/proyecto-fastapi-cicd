import pytest
from pydantic import ValidationError

from src.app.schemas.user import UserCreate


class TestUserCreateSchema:
    def test_valid_user_creation(self):
        user = UserCreate(email="test@example.com", password="Valid123!")
        assert user.email == "test@example.com"

    def test_invalid_email_raises_error(self):
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(email="not-an-email", password="Valid123!")
        assert "email" in str(exc_info.value)

    def test_weak_password_raises_error(self):
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(email="test@example.com", password="weak")
        assert "password" in str(exc_info.value)

    @pytest.mark.parametrize("email", [
        "user@domain.com",
        "user+tag@domain.co.uk",
        "user.name@subdomain.domain.org",
    ])
    def test_valid_email_formats(self, email: str):
        user = UserCreate(email=email, password="Valid123!")
        assert user.email == email
