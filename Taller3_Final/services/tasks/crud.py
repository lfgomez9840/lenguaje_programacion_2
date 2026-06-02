"""Operaciones CRUD para el servicio de tareas."""

from sqlalchemy.orm import Session

from .models import Task
from .schemas import TaskCreate, TaskUpdate


def get_task(db: Session, task_id: int) -> Task | None:
    """Obtiene una tarea por su ID."""
    return db.query(Task).filter(Task.id == task_id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 100) -> list[Task]:
    """Obtiene una lista de tareas con paginación."""
    return db.query(Task).offset(skip).limit(limit).all()


def get_tasks_by_project(
    db: Session, project_id: int, skip: int = 0, limit: int = 100
) -> list[Task]:
    """Obtiene las tareas de un proyecto específico."""
    return (
        db.query(Task)
        .filter(Task.project_id == project_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_tasks_by_user(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> list[Task]:
    """Obtiene las tareas asignadas a un usuario específico."""
    return (
        db.query(Task)
        .filter(Task.assigned_to == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_task(db: Session, task: TaskCreate) -> Task:
    """Crea una nueva tarea en la base de datos."""
    db_task = Task(
        title=task.title,
        description=task.description,
        project_id=task.project_id,
        assigned_to=task.assigned_to,
        status=task.status.value,
        priority=task.priority.value,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task_update: TaskUpdate) -> Task | None:
    """Actualiza una tarea existente."""
    db_task = get_task(db, task_id)
    if db_task is None:
        return None

    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(value, "value"):
            value = value.value
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    """Elimina una tarea por su ID."""
    db_task = get_task(db, task_id)
    if db_task is None:
        return False
    db.delete(db_task)
    db.commit()
    return True
