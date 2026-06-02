"""Frontend Flask para el sistema de gestión de tareas y proyectos."""

import os

import requests
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "clave-secreta-desarrollo")

# URL del API Gateway
API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://api-gateway:8000")


def api_request(method, endpoint, json=None):
    """Realiza una petición al API Gateway y retorna la respuesta."""
    url = f"{API_GATEWAY_URL}{endpoint}"
    try:
        response = requests.request(method, url, json=json, timeout=10)
        return response
    except requests.ConnectionError:
        return None
    except requests.Timeout:
        return None


# ===================== RUTAS PRINCIPALES =====================


@app.route("/")
def index():
    """Página de inicio del sistema."""
    return render_template("index.html")


# ===================== RUTAS DE USUARIOS =====================


@app.route("/usuarios")
def list_usuarios():
    """Lista todos los usuarios del sistema."""
    response = api_request("GET", "/api/users/users/")
    usuarios = response.json() if response and response.ok else []
    return render_template("usuarios.html", usuarios=usuarios)


@app.route("/usuarios/crear", methods=["POST"])
def crear_usuario():
    """Crea un nuevo usuario en el sistema."""
    data = {
        "username": request.form["username"],
        "email": request.form["email"],
        "password": request.form["password"],
    }
    response = api_request("POST", "/api/users/users/", json=data)
    if response and response.status_code == 201:
        flash("Usuario creado exitosamente", "success")
    else:
        detail = "Error al crear usuario"
        if response:
            resp_data = response.json()
            detail = resp_data.get("detail", detail)
        flash(detail, "error")
    return redirect(url_for("list_usuarios"))


@app.route("/usuarios/eliminar/<int:user_id>", methods=["POST"])
def eliminar_usuario(user_id):
    """Elimina un usuario del sistema."""
    response = api_request("DELETE", f"/api/users/users/{user_id}")
    if response and response.ok:
        flash("Usuario eliminado exitosamente", "success")
    else:
        flash("Error al eliminar usuario", "error")
    return redirect(url_for("list_usuarios"))


# ===================== RUTAS DE PROYECTOS =====================


@app.route("/proyectos")
def list_proyectos():
    """Lista todos los proyectos del sistema."""
    response = api_request("GET", "/api/projects/projects/")
    proyectos = response.json() if response and response.ok else []
    return render_template("proyectos.html", proyectos=proyectos)


@app.route("/proyectos/crear", methods=["POST"])
def crear_proyecto():
    """Crea un nuevo proyecto en el sistema."""
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "owner_id": int(request.form["owner_id"]),
    }
    response = api_request("POST", "/api/projects/projects/", json=data)
    if response and response.status_code == 201:
        flash("Proyecto creado exitosamente", "success")
    else:
        detail = "Error al crear proyecto"
        if response:
            resp_data = response.json()
            detail = resp_data.get("detail", detail)
        flash(detail, "error")
    return redirect(url_for("list_proyectos"))


@app.route("/proyectos/eliminar/<int:project_id>", methods=["POST"])
def eliminar_proyecto(project_id):
    """Elimina un proyecto del sistema."""
    response = api_request("DELETE", f"/api/projects/projects/{project_id}")
    if response and response.ok:
        flash("Proyecto eliminado exitosamente", "success")
    else:
        flash("Error al eliminar proyecto", "error")
    return redirect(url_for("list_proyectos"))


# ===================== RUTAS DE TAREAS =====================


@app.route("/tareas")
def list_tareas():
    """Lista todas las tareas del sistema."""
    response = api_request("GET", "/api/tasks/tasks/")
    tareas = response.json() if response and response.ok else []
    return render_template("tareas.html", tareas=tareas)


@app.route("/tareas/crear", methods=["POST"])
def crear_tarea():
    """Crea una nueva tarea en el sistema."""
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "project_id": int(request.form["project_id"]),
        "status": request.form.get("status", "pendiente"),
        "priority": request.form.get("priority", "media"),
    }
    assigned = request.form.get("assigned_to")
    if assigned:
        data["assigned_to"] = int(assigned)

    response = api_request("POST", "/api/tasks/tasks/", json=data)
    if response and response.status_code == 201:
        flash("Tarea creada exitosamente", "success")
    else:
        detail = "Error al crear tarea"
        if response:
            resp_data = response.json()
            detail = resp_data.get("detail", detail)
        flash(detail, "error")
    return redirect(url_for("list_tareas"))


@app.route("/tareas/eliminar/<int:task_id>", methods=["POST"])
def eliminar_tarea(task_id):
    """Elimina una tarea del sistema."""
    response = api_request("DELETE", f"/api/tasks/tasks/{task_id}")
    if response and response.ok:
        flash("Tarea eliminada exitosamente", "success")
    else:
        flash("Error al eliminar tarea", "error")
    return redirect(url_for("list_tareas"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
