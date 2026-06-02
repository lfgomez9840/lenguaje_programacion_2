"""Esquemas Pydantic para el servicio de usuarios."""

from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Esquema base de usuario."""

    username: str
    email: EmailStr


class UserCreate(UserBase):
    """Esquema para crear un usuario."""

    password: str


class UserUpdate(BaseModel):
    """Esquema para actualizar un usuario."""

    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    """Esquema de respuesta de usuario."""

    id: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    """Esquema para solicitud de login."""

    username: str
    password: str


class LoginResponse(BaseModel):
    """Esquema de respuesta de login."""

    message: str
    user_id: int
    username: str
