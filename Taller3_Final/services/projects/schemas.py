"""Esquemas Pydantic para el servicio de proyectos."""

from datetime import datetime

from pydantic import BaseModel


class ProjectBase(BaseModel):
    """Esquema base de proyecto."""

    name: str
    description: str | None = None
    owner_id: int


class ProjectCreate(ProjectBase):
    """Esquema para crear un proyecto."""

    pass


class ProjectUpdate(BaseModel):
    """Esquema para actualizar un proyecto."""

    name: str | None = None
    description: str | None = None
    owner_id: int | None = None


class ProjectResponse(ProjectBase):
    """Esquema de respuesta de proyecto."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
