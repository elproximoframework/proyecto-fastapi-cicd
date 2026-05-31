import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class UserBase(BaseModel):
    email: str = Field(..., examples=["user@domain.com"])
    full_name: Optional[str] = Field(None, examples=["John Doe"])
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str = Field(..., examples=["StrongPassword123!"])

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, value: str) -> str:
        # Validación robusta de formato de correo
        email_regex = r"^[\w\.\+-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, value):
            raise ValueError("email format is invalid")
        return value

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        # Validación de contraseña fuerte
        if len(value) < 8:
            raise ValueError("password must be at least 8 characters long")
        if not re.search(r"[A-Z]", value):
            raise ValueError("password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("password must contain at least one lowercase letter")
        if not re.search(r"\d", value):
            raise ValueError("password must contain at least one digit")
        return value


class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    full_name: Optional[str] = None


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
