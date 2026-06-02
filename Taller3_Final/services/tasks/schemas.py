"""Esquemas Pydantic para el servicio de tareas."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class TaskStatus(str, Enum):
    """Estados posibles de una tarea."""

    PENDIENTE = "pendiente"
    EN_PROGRESO = "en_progreso"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"


class TaskPriority(str, Enum):
    """Niveles de prioridad de una tarea."""

    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"


class TaskBase(BaseModel):
    """Esquema base de tarea."""

    title: str
    description: str | None = None
    project_id: int
    assigned_to: int | None = None
    status: TaskStatus = TaskStatus.PENDIENTE
    priority: TaskPriority = TaskPriority.MEDIA


class TaskCreate(TaskBase):
    """Esquema para crear una tarea."""

    pass


class TaskUpdate(BaseModel):
    """Esquema para actualizar una tarea."""

    title: str | None = None
    description: str | None = None
    assigned_to: int | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None


class TaskResponse(TaskBase):
    """Esquema de respuesta de tarea."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
