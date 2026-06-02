"""Operaciones CRUD para el servicio de usuarios."""

import hashlib

from sqlalchemy.orm import Session

from .models import User
from .schemas import UserCreate, UserUpdate


def hash_password(password: str) -> str:
    """Genera un hash simple de la contraseña usando SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def get_user(db: Session, user_id: int) -> User | None:
    """Obtiene un usuario por su ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    """Obtiene un usuario por su nombre de usuario."""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    """Obtiene un usuario por su email."""
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """Obtiene una lista de usuarios con paginación."""
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    """Crea un nuevo usuario en la base de datos."""
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> User | None:
    """Actualiza un usuario existente."""
    db_user = get_user(db, user_id)
    if db_user is None:
        return None

    update_data = user_update.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))

    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """Elimina un usuario por su ID."""
    db_user = get_user(db, user_id)
    if db_user is None:
        return False
    db.delete(db_user)
    db.commit()
    return True


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    """Autentica un usuario verificando sus credenciales."""
    db_user = get_user_by_username(db, username)
    if db_user is None:
        return None
    if db_user.hashed_password != hash_password(password):
        return None
    return db_user
