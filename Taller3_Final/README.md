# 📋 Sistema de Gestión de Tareas y Proyectos — Microservicios

> **Equipo del Poder** — Diego Benitez & Luis Felipe Gomez
>
> Corporación Universitaria Remington — Lenguaje de Programación 2

---

## 📖 Descripción

Sistema completo de gestión de tareas y proyectos construido con una **arquitectura de microservicios**. Permite administrar usuarios, crear proyectos y asignar tareas con diferentes estados y prioridades. Incluye un API Gateway centralizado y un frontend web interactivo.

## 🏗️ Arquitectura

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Frontend    │────▶│  API Gateway │────▶│  Users Service  │──▶ PostgreSQL
│  (Flask)     │     │  (FastAPI)   │     │  (FastAPI)      │
│  :5000       │     │  :8000       │     │  :8001          │
└─────────────┘     │              │     └─────────────────┘
                    │              │     ┌─────────────────┐
                    │              │────▶│ Projects Service │──▶ PostgreSQL
                    │              │     │  (FastAPI)       │
                    │              │     │  :8002           │
                    │              │     └─────────────────┘
                    │              │     ┌─────────────────┐
                    │              │────▶│  Tasks Service   │──▶ PostgreSQL
                    └──────────────┘     │  (FastAPI)       │
                                        │  :8003           │
                                        └─────────────────┘
```

Consulta [`ARQUITECTURA.md`](ARQUITECTURA.md) para una explicación detallada del diseño.

## 🛠️ Tecnologías

| Componente | Tecnología |
|---|---|
| Microservicios | FastAPI + SQLAlchemy |
| Base de datos | PostgreSQL 16 |
| API Gateway | FastAPI + HTTPX |
| Frontend | Flask + Jinja2 + CSS |
| Contenedores | Docker + Docker Compose |
| Control de calidad | Ruff + Pytest + Pre-commit |
| CI/CD | GitHub Actions |

## 🚀 Instalación y Ejecución

### Prerrequisitos

- [Docker](https://docs.docker.com/get-docker/) y [Docker Compose](https://docs.docker.com/compose/install/) instalados.

### Pasos

1. **Clonar el repositorio:**

```bash
git clone https://github.com/lfgomez9840/lenguaje_programacion_2.git
cd lenguaje_programacion_2/Taller3_Final
```

2. **Configurar variables de entorno (opcional):**

```bash
cp .env.example .env
# Editar .env si se necesitan valores personalizados
```

3. **Levantar todos los servicios con Docker Compose:**

```bash
docker-compose up --build
```

4. **Acceder a la aplicación:**

| Servicio | URL |
|---|---|
| Frontend | http://localhost:5000 |
| API Gateway | http://localhost:8000 |
| API Gateway Docs | http://localhost:8000/docs |
| Servicio de Usuarios | http://localhost:8001/docs |
| Servicio de Proyectos | http://localhost:8002/docs |
| Servicio de Tareas | http://localhost:8003/docs |

5. **Detener los servicios:**

```bash
docker-compose down
# Para eliminar también los volúmenes de datos:
docker-compose down -v
```

## 📡 Endpoints de los Servicios

### Servicio de Usuarios (`:8001`)

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/health` | Verificar salud del servicio |
| `POST` | `/users/` | Crear un nuevo usuario |
| `GET` | `/users/` | Listar todos los usuarios |
| `GET` | `/users/{id}` | Obtener usuario por ID |
| `PUT` | `/users/{id}` | Actualizar usuario |
| `DELETE` | `/users/{id}` | Eliminar usuario |
| `POST` | `/login` | Autenticar usuario |

### Servicio de Proyectos (`:8002`)

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/health` | Verificar salud del servicio |
| `POST` | `/projects/` | Crear un nuevo proyecto |
| `GET` | `/projects/` | Listar todos los proyectos |
| `GET` | `/projects/{id}` | Obtener proyecto por ID |
| `GET` | `/projects/owner/{id}` | Proyectos por propietario |
| `PUT` | `/projects/{id}` | Actualizar proyecto |
| `DELETE` | `/projects/{id}` | Eliminar proyecto |

### Servicio de Tareas (`:8003`)

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/health` | Verificar salud del servicio |
| `POST` | `/tasks/` | Crear una nueva tarea |
| `GET` | `/tasks/` | Listar todas las tareas |
| `GET` | `/tasks/{id}` | Obtener tarea por ID |
| `GET` | `/tasks/project/{id}` | Tareas por proyecto |
| `GET` | `/tasks/user/{id}` | Tareas por usuario asignado |
| `PUT` | `/tasks/{id}` | Actualizar tarea |
| `DELETE` | `/tasks/{id}` | Eliminar tarea |

### API Gateway (`:8000`)

Todas las rutas se acceden con el prefijo `/api/{servicio}/`:

```
/api/users/users/        → Servicio de Usuarios
/api/projects/projects/  → Servicio de Proyectos
/api/tasks/tasks/        → Servicio de Tareas
```

## 🧪 Tests y Control de Calidad

### Ejecutar tests localmente

```bash
pip install -r requirements-dev.txt
pytest -v
```

### Ejecutar linting y formateo

```bash
ruff check .          # Verificar linting
ruff format --check . # Verificar formato
ruff format .         # Formatear automáticamente
```

### Pre-commit hooks

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

### GitHub Actions

El workflow de CI/CD se ejecuta automáticamente al crear un tag con el formato `v*` (ej: `v1.0.0`). Ejecuta:

1. Linting con Ruff
2. Verificación de formato con Ruff
3. Tests con Pytest

## 📂 Estructura del Proyecto

```
Taller3_Final/
├── .github/workflows/     # Workflow de GitHub Actions
│   └── checks.yml
├── api-gateway/           # API Gateway centralizado
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── common/                # Utilidades compartidas
│   ├── __init__.py
│   └── utils.py
├── frontend/              # Frontend web con Flask
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── usuarios.html
│   │   ├── proyectos.html
│   │   └── tareas.html
│   ├── static/css/
│   │   └── style.css
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── services/              # Microservicios
│   ├── users/             # Servicio de usuarios
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── crud.py
│   │   ├── database.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── projects/          # Servicio de proyectos
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── crud.py
│   │   ├── database.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── tasks/             # Servicio de tareas
│       ├── main.py
│       ├── models.py
│       ├── schemas.py
│       ├── crud.py
│       ├── database.py
│       ├── requirements.txt
│       └── Dockerfile
├── tests/                 # Tests del proyecto
│   ├── conftest.py
│   └── test_main.py
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── docker-compose.yml
├── pyproject.toml
├── requirements-dev.txt
├── ARQUITECTURA.md
└── README.md
```

## 👥 Equipo

| Integrante | Rol |
|---|---|
| **Diego Benitez** | Desarrollador |
| **Luis Felipe Gomez** | Desarrollador |

---

*Corporación Universitaria Remington — Lenguaje de Programación 2 — 2026*
