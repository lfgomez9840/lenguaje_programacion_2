"""API Gateway - Punto de entrada central para los microservicios."""

import os

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# URLs de los microservicios (configurables por variables de entorno)
USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL", "http://users-service:8001")
PROJECTS_SERVICE_URL = os.getenv("PROJECTS_SERVICE_URL", "http://projects-service:8002")
TASKS_SERVICE_URL = os.getenv("TASKS_SERVICE_URL", "http://tasks-service:8003")

app = FastAPI(
    title="API Gateway - Sistema de Gestión de Tareas",
    description=(
        "Punto de entrada central que enruta las peticiones "
        "a los microservicios correspondientes."
    ),
    version="1.0.0",
)

# Configurar CORS para permitir peticiones del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Mapeo de rutas a servicios
SERVICE_MAP = {
    "users": USERS_SERVICE_URL,
    "projects": PROJECTS_SERVICE_URL,
    "tasks": TASKS_SERVICE_URL,
}


@app.get("/health")
def health_check():
    """Endpoint de verificación de salud del gateway."""
    return {"status": "ok", "service": "api-gateway"}


@app.get("/services")
def list_services():
    """Lista los microservicios disponibles y sus URLs."""
    return {
        "services": {
            "users": f"{USERS_SERVICE_URL}",
            "projects": f"{PROJECTS_SERVICE_URL}",
            "tasks": f"{TASKS_SERVICE_URL}",
        }
    }


async def _proxy_request(service_url: str, path: str, request: Request) -> JSONResponse:
    """Reenvía una petición HTTP al microservicio correspondiente."""
    url = f"{service_url}/{path}"
    headers = dict(request.headers)
    headers.pop("host", None)

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            body = await request.body()
            response = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                content=body,
                params=dict(request.query_params),
            )
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code,
            )
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail=f"El servicio no está disponible: {service_url}",
        )
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Tiempo de espera agotado al conectar con el servicio",
        )


@app.api_route(
    "/api/{service}/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
)
async def gateway_proxy(service: str, path: str, request: Request):
    """Enruta las peticiones al microservicio correspondiente.

    Las rutas siguen el formato: /api/{servicio}/{ruta_del_servicio}
    Ejemplo: /api/users/users/ -> http://users-service:8001/users/
    """
    if service not in SERVICE_MAP:
        raise HTTPException(
            status_code=404,
            detail=f"Servicio '{service}' no encontrado. "
            f"Servicios disponibles: {list(SERVICE_MAP.keys())}",
        )

    service_url = SERVICE_MAP[service]
    return await _proxy_request(service_url, path, request)
