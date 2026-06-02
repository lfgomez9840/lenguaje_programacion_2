"""Microservicio de gestión de proyectos - API FastAPI."""

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .crud import (
    create_project,
    delete_project,
    get_project,
    get_projects,
    get_projects_by_owner,
    update_project,
)
from .database import Base, engine, get_db
from .schemas import ProjectCreate, ProjectResponse, ProjectUpdate

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Servicio de Proyectos",
    description="Microservicio para la gestión de proyectos del sistema.",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    """Endpoint de verificación de salud del servicio."""
    return {"status": "ok", "service": "projects"}


@app.post("/projects/", response_model=ProjectResponse, status_code=201)
def create_new_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """Crea un nuevo proyecto en el sistema."""
    return create_project(db, project)


@app.get("/projects/", response_model=list[ProjectResponse])
def list_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos los proyectos con paginación."""
    return get_projects(db, skip=skip, limit=limit)


@app.get("/projects/{project_id}", response_model=ProjectResponse)
def read_project(project_id: int, db: Session = Depends(get_db)):
    """Obtiene un proyecto específico por su ID."""
    db_project = get_project(db, project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return db_project


@app.get("/projects/owner/{owner_id}", response_model=list[ProjectResponse])
def list_projects_by_owner(
    owner_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Lista los proyectos de un usuario específico."""
    return get_projects_by_owner(db, owner_id, skip=skip, limit=limit)


@app.put("/projects/{project_id}", response_model=ProjectResponse)
def update_existing_project(
    project_id: int, project_update: ProjectUpdate, db: Session = Depends(get_db)
):
    """Actualiza la información de un proyecto existente."""
    db_project = update_project(db, project_id, project_update)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return db_project


@app.delete("/projects/{project_id}")
def delete_existing_project(project_id: int, db: Session = Depends(get_db)):
    """Elimina un proyecto del sistema."""
    if not delete_project(db, project_id):
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return {"message": "Proyecto eliminado exitosamente"}
