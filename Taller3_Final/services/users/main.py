"""Microservicio de gestión de usuarios - API FastAPI."""

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .crud import (
    authenticate_user,
    create_user,
    delete_user,
    get_user,
    get_user_by_email,
    get_user_by_username,
    get_users,
    update_user,
)
from .database import Base, engine, get_db
from .schemas import (
    LoginRequest,
    LoginResponse,
    UserCreate,
    UserResponse,
    UserUpdate,
)

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Servicio de Usuarios",
    description="Microservicio para la gestión de usuarios del sistema.",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    """Endpoint de verificación de salud del servicio."""
    return {"status": "ok", "service": "users"}


@app.post("/users/", response_model=UserResponse, status_code=201)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    """Crea un nuevo usuario en el sistema."""
    # Verificar si el username ya existe
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
    # Verificar si el email ya existe
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    return create_user(db, user)


@app.get("/users/", response_model=list[UserResponse])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos los usuarios con paginación."""
    return get_users(db, skip=skip, limit=limit)


@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Obtiene un usuario específico por su ID."""
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user


@app.put("/users/{user_id}", response_model=UserResponse)
def update_existing_user(
    user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)
):
    """Actualiza la información de un usuario existente."""
    db_user = update_user(db, user_id, user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user


@app.delete("/users/{user_id}")
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    """Elimina un usuario del sistema."""
    if not delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado exitosamente"}


@app.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Autentica un usuario con sus credenciales."""
    user = authenticate_user(db, login_data.username, login_data.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return LoginResponse(
        message="Login exitoso",
        user_id=user.id,
        username=user.username,
    )
