"""Configuración de la base de datos para el servicio de usuarios."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# URL de conexión a PostgreSQL (configurable por variable de entorno)
DATABASE_URL = os.getenv(
    "USERS_DATABASE_URL",
    "postgresql://postgres:postgres@users-db:5432/users_db",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Clase base para los modelos de SQLAlchemy."""

    pass


def get_db():
    """Generador de sesiones de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
