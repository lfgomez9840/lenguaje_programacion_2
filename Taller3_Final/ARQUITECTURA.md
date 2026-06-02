# 🏗️ Arquitectura de Microservicios

## Descripción General

El sistema de gestión de tareas y proyectos implementa una **arquitectura de microservicios**, donde cada servicio es una aplicación independiente con su propia base de datos, siguiendo el principio de **Database per Service**.

## Componentes

### 1. API Gateway (`api-gateway/`)

- **Tecnología:** FastAPI + HTTPX
- **Puerto:** 8000
- **Función:** Punto de entrada único para todas las peticiones del frontend. Enruta cada solicitud al microservicio correspondiente usando un proxy inverso asíncrono.
- **Patrón:** API Gateway Pattern

### 2. Servicio de Usuarios (`services/users/`)

- **Tecnología:** FastAPI + SQLAlchemy
- **Puerto:** 8001
- **Base de datos:** PostgreSQL (`users_db`)
- **Responsabilidades:**
  - Registro de usuarios
  - Autenticación (login)
  - CRUD completo de usuarios
  - Hashing de contraseñas con SHA-256

### 3. Servicio de Proyectos (`services/projects/`)

- **Tecnología:** FastAPI + SQLAlchemy
- **Puerto:** 8002
- **Base de datos:** PostgreSQL (`projects_db`)
- **Responsabilidades:**
  - CRUD completo de proyectos
  - Consulta de proyectos por propietario
  - Vinculación lógica con el servicio de usuarios mediante `owner_id`

### 4. Servicio de Tareas (`services/tasks/`)

- **Tecnología:** FastAPI + SQLAlchemy
- **Puerto:** 8003
- **Base de datos:** PostgreSQL (`tasks_db`)
- **Responsabilidades:**
  - CRUD completo de tareas
  - Gestión de estados: pendiente, en progreso, completada, cancelada
  - Gestión de prioridades: baja, media, alta, crítica
  - Consulta de tareas por proyecto y por usuario asignado
  - Vinculación lógica con proyectos (`project_id`) y usuarios (`assigned_to`)

### 5. Frontend (`frontend/`)

- **Tecnología:** Flask + Jinja2 + CSS
- **Puerto:** 5000
- **Función:** Interfaz web que permite a los usuarios interactuar con el sistema a través del API Gateway.

## Patrones de Diseño Aplicados

| Patrón | Descripción |
|---|---|
| **Database per Service** | Cada microservicio tiene su propia base de datos PostgreSQL |
| **API Gateway** | Un único punto de entrada que enruta peticiones a los servicios |
| **Proxy Pattern** | El gateway actúa como proxy inverso hacia los microservicios |
| **Repository Pattern** | Módulos CRUD encapsulan el acceso a datos |
| **DTO Pattern** | Esquemas Pydantic para validación y transferencia de datos |

## Comunicación entre Servicios

- **Frontend → API Gateway:** HTTP/REST síncrono
- **API Gateway → Microservicios:** HTTP/REST síncrono mediante proxy HTTPX
- **Microservicios → Base de datos:** Conexión directa PostgreSQL vía SQLAlchemy

## Orquestación con Docker

Docker Compose gestiona todo el ecosistema:

- **3 contenedores de PostgreSQL** (uno por microservicio)
- **3 contenedores de microservicios** (usuarios, proyectos, tareas)
- **1 contenedor de API Gateway**
- **1 contenedor de Frontend**

### Redes

- `backend`: Conecta los microservicios con sus bases de datos y el API Gateway
- `frontend`: Conecta el frontend con el API Gateway

### Healthchecks

Las bases de datos tienen healthchecks configurados para asegurar que los microservicios solo arranquen cuando la base de datos esté lista.

## Control de Calidad

- **Ruff:** Linting y formateo automático del código Python
- **Pytest:** Tests unitarios con TestClient de FastAPI y SQLite en memoria
- **Pre-commit:** Hooks que verifican calidad antes de cada commit
- **GitHub Actions:** Pipeline de CI que se ejecuta al crear tags `v*`

## Diagrama de Flujo

```
Usuario
  │
  ▼
Frontend (Flask :5000)
  │
  ▼ HTTP
API Gateway (FastAPI :8000)
  │
  ├──▶ /api/users/*    → Users Service (:8001)    → PostgreSQL (users_db)
  ├──▶ /api/projects/* → Projects Service (:8002) → PostgreSQL (projects_db)
  └──▶ /api/tasks/*    → Tasks Service (:8003)    → PostgreSQL (tasks_db)
```

---

*Equipo del Poder — Diego Benitez & Luis Felipe Gomez*
*Corporación Universitaria Remington — Lenguaje de Programación 2*
