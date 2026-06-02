"""Utilidades compartidas entre los microservicios."""

from datetime import datetime, timezone


def get_current_timestamp() -> datetime:
    """Retorna la fecha y hora actual en UTC."""
    return datetime.now(timezone.utc)


def format_response(data: dict, message: str = "OK", status: int = 200) -> dict:
    """Formatea una respuesta estándar para los microservicios."""
    return {
        "status": status,
        "message": message,
        "data": data,
    }


def format_error(message: str, status: int = 400) -> dict:
    """Formatea una respuesta de error estándar."""
    return {
        "status": status,
        "message": message,
        "data": None,
    }
