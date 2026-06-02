"""Operaciones CRUD para el servicio de proyectos."""

from sqlalchemy.orm import Session

from .models import Project
from .schemas import ProjectCreate, ProjectUpdate


def get_project(db: Session, project_id: int) -> Project | None:
    """Obtiene un proyecto por su ID."""
    return db.query(Project).filter(Project.id == project_id).first()


def get_projects(db: Session, skip: int = 0, limit: int = 100) -> list[Project]:
    """Obtiene una lista de proyectos con paginación."""
    return db.query(Project).offset(skip).limit(limit).all()


def get_projects_by_owner(
    db: Session, owner_id: int, skip: int = 0, limit: int = 100
) -> list[Project]:
    """Obtiene los proyectos de un usuario específico."""
    return (
        db.query(Project)
        .filter(Project.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_project(db: Session, project: ProjectCreate) -> Project:
    """Crea un nuevo proyecto en la base de datos."""
    db_project = Project(
        name=project.name,
        description=project.description,
        owner_id=project.owner_id,
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(
    db: Session, project_id: int, project_update: ProjectUpdate
) -> Project | None:
    """Actualiza un proyecto existente."""
    db_project = get_project(db, project_id)
    if db_project is None:
        return None

    update_data = project_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)

    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int) -> bool:
    """Elimina un proyecto por su ID."""
    db_project = get_project(db, project_id)
    if db_project is None:
        return False
    db.delete(db_project)
    db.commit()
    return True
