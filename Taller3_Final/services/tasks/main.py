"""Microservicio de gestión de tareas - API FastAPI."""

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .crud import (
    create_task,
    delete_task,
    get_task,
    get_tasks,
    get_tasks_by_project,
    get_tasks_by_user,
    update_task,
)
from .database import Base, engine, get_db
from .schemas import TaskCreate, TaskResponse, TaskUpdate

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Servicio de Tareas",
    description="Microservicio para la gestión de tareas del sistema.",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    """Endpoint de verificación de salud del servicio."""
    return {"status": "ok", "service": "tasks"}


@app.post("/tasks/", response_model=TaskResponse, status_code=201)
def create_new_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Crea una nueva tarea en el sistema."""
    return create_task(db, task)


@app.get("/tasks/", response_model=list[TaskResponse])
def list_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todas las tareas con paginación."""
    return get_tasks(db, skip=skip, limit=limit)


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    """Obtiene una tarea específica por su ID."""
    db_task = get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_task


@app.get("/tasks/project/{project_id}", response_model=list[TaskResponse])
def list_tasks_by_project(
    project_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Lista las tareas de un proyecto específico."""
    return get_tasks_by_project(db, project_id, skip=skip, limit=limit)


@app.get("/tasks/user/{user_id}", response_model=list[TaskResponse])
def list_tasks_by_user(
    user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Lista las tareas asignadas a un usuario específico."""
    return get_tasks_by_user(db, user_id, skip=skip, limit=limit)


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_existing_task(
    task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)
):
    """Actualiza la información de una tarea existente."""
    db_task = update_task(db, task_id, task_update)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_task


@app.delete("/tasks/{task_id}")
def delete_existing_task(task_id: int, db: Session = Depends(get_db)):
    """Elimina una tarea del sistema."""
    if not delete_task(db, task_id):
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"message": "Tarea eliminada exitosamente"}
