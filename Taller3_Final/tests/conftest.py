"""Configuración de fixtures para pytest."""

import os
import sys

# Configurar variables de entorno ANTES de importar los módulos de servicios
# para que usen SQLite en memoria en lugar de PostgreSQL
os.environ["USERS_DATABASE_URL"] = "sqlite://"
os.environ["PROJECTS_DATABASE_URL"] = "sqlite://"
os.environ["TASKS_DATABASE_URL"] = "sqlite://"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import StaticPool, create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.projects.database import Base as ProjectsBase  # noqa: E402
from services.projects.database import get_db as projects_get_db  # noqa: E402
from services.projects.main import app as projects_app  # noqa: E402
from services.tasks.database import Base as TasksBase  # noqa: E402
from services.tasks.database import get_db as tasks_get_db  # noqa: E402
from services.tasks.main import app as tasks_app  # noqa: E402
from services.users.database import Base as UsersBase  # noqa: E402
from services.users.database import get_db as users_get_db  # noqa: E402
from services.users.main import app as users_app  # noqa: E402


def _create_test_db(base_class):
    """Crea una base de datos SQLite en memoria para pruebas."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    base_class.metadata.create_all(bind=engine)
    return testing_session


@pytest.fixture()
def users_client():
    """Cliente de prueba para el servicio de usuarios."""
    testing_session = _create_test_db(UsersBase)

    def override_get_db():
        db = testing_session()
        try:
            yield db
        finally:
            db.close()

    users_app.dependency_overrides[users_get_db] = override_get_db
    with TestClient(users_app) as client:
        yield client
    users_app.dependency_overrides.clear()


@pytest.fixture()
def projects_client():
    """Cliente de prueba para el servicio de proyectos."""
    testing_session = _create_test_db(ProjectsBase)

    def override_get_db():
        db = testing_session()
        try:
            yield db
        finally:
            db.close()

    projects_app.dependency_overrides[projects_get_db] = override_get_db
    with TestClient(projects_app) as client:
        yield client
    projects_app.dependency_overrides.clear()


@pytest.fixture()
def tasks_client():
    """Cliente de prueba para el servicio de tareas."""
    testing_session = _create_test_db(TasksBase)

    def override_get_db():
        db = testing_session()
        try:
            yield db
        finally:
            db.close()

    tasks_app.dependency_overrides[tasks_get_db] = override_get_db
    with TestClient(tasks_app) as client:
        yield client
    tasks_app.dependency_overrides.clear()
