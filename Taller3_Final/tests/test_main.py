"""Tests principales para los microservicios del sistema de gestión."""


class TestSanity:
    """Pruebas básicas de salud del proyecto."""

    def test_suma(self):
        assert 5 + 3 == 8

    def test_par(self):
        assert (4 % 2) == 0


# ===================== TESTS DEL SERVICIO DE USUARIOS =====================


class TestUsersService:
    """Pruebas para el microservicio de usuarios."""

    def test_health_check(self, users_client):
        """Verifica que el servicio de usuarios está activo."""
        response = users_client.get("/health")
        assert response.status_code == 200
        assert response.json()["service"] == "users"

    def test_create_user(self, users_client):
        """Verifica la creación de un nuevo usuario."""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        }
        response = users_client.post("/users/", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert data["is_active"] is True
        assert "id" in data

    def test_create_user_duplicate_username(self, users_client):
        """Verifica que no se puede crear un usuario con username duplicado."""
        user_data = {
            "username": "duplicado",
            "email": "user1@example.com",
            "password": "pass123",
        }
        users_client.post("/users/", json=user_data)
        user_data["email"] = "user2@example.com"
        response = users_client.post("/users/", json=user_data)
        assert response.status_code == 400

    def test_list_users(self, users_client):
        """Verifica que se pueden listar los usuarios."""
        response = users_client.get("/users/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_user_by_id(self, users_client):
        """Verifica que se puede obtener un usuario por su ID."""
        user_data = {
            "username": "getuser",
            "email": "getuser@example.com",
            "password": "pass123",
        }
        create_resp = users_client.post("/users/", json=user_data)
        user_id = create_resp.json()["id"]

        response = users_client.get(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["username"] == "getuser"

    def test_get_user_not_found(self, users_client):
        """Verifica que se retorna 404 para un usuario inexistente."""
        response = users_client.get("/users/9999")
        assert response.status_code == 404

    def test_update_user(self, users_client):
        """Verifica la actualización de un usuario."""
        user_data = {
            "username": "updateuser",
            "email": "update@example.com",
            "password": "pass123",
        }
        create_resp = users_client.post("/users/", json=user_data)
        user_id = create_resp.json()["id"]

        update_data = {"username": "updated_name"}
        response = users_client.put(f"/users/{user_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["username"] == "updated_name"

    def test_delete_user(self, users_client):
        """Verifica la eliminación de un usuario."""
        user_data = {
            "username": "deleteuser",
            "email": "delete@example.com",
            "password": "pass123",
        }
        create_resp = users_client.post("/users/", json=user_data)
        user_id = create_resp.json()["id"]

        response = users_client.delete(f"/users/{user_id}")
        assert response.status_code == 200

        # Verificar que ya no existe
        response = users_client.get(f"/users/{user_id}")
        assert response.status_code == 404

    def test_login_success(self, users_client):
        """Verifica el login exitoso de un usuario."""
        user_data = {
            "username": "loginuser",
            "email": "login@example.com",
            "password": "secretpass",
        }
        users_client.post("/users/", json=user_data)

        login_data = {"username": "loginuser", "password": "secretpass"}
        response = users_client.post("/login", json=login_data)
        assert response.status_code == 200
        assert response.json()["message"] == "Login exitoso"

    def test_login_invalid_credentials(self, users_client):
        """Verifica que credenciales inválidas retornan error."""
        login_data = {"username": "noexiste", "password": "wrongpass"}
        response = users_client.post("/login", json=login_data)
        assert response.status_code == 401


# ===================== TESTS DEL SERVICIO DE PROYECTOS =====================


class TestProjectsService:
    """Pruebas para el microservicio de proyectos."""

    def test_health_check(self, projects_client):
        """Verifica que el servicio de proyectos está activo."""
        response = projects_client.get("/health")
        assert response.status_code == 200
        assert response.json()["service"] == "projects"

    def test_create_project(self, projects_client):
        """Verifica la creación de un nuevo proyecto."""
        project_data = {
            "name": "Proyecto Test",
            "description": "Un proyecto de prueba",
            "owner_id": 1,
        }
        response = projects_client.post("/projects/", json=project_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Proyecto Test"
        assert data["owner_id"] == 1

    def test_list_projects(self, projects_client):
        """Verifica que se pueden listar los proyectos."""
        response = projects_client.get("/projects/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_project_by_id(self, projects_client):
        """Verifica que se puede obtener un proyecto por su ID."""
        project_data = {
            "name": "Mi Proyecto",
            "description": "Descripción",
            "owner_id": 1,
        }
        create_resp = projects_client.post("/projects/", json=project_data)
        project_id = create_resp.json()["id"]

        response = projects_client.get(f"/projects/{project_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Mi Proyecto"

    def test_get_project_not_found(self, projects_client):
        """Verifica que se retorna 404 para un proyecto inexistente."""
        response = projects_client.get("/projects/9999")
        assert response.status_code == 404

    def test_update_project(self, projects_client):
        """Verifica la actualización de un proyecto."""
        project_data = {
            "name": "Original",
            "description": "Desc original",
            "owner_id": 1,
        }
        create_resp = projects_client.post("/projects/", json=project_data)
        project_id = create_resp.json()["id"]

        update_data = {"name": "Actualizado"}
        response = projects_client.put(f"/projects/{project_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["name"] == "Actualizado"

    def test_delete_project(self, projects_client):
        """Verifica la eliminación de un proyecto."""
        project_data = {"name": "Eliminar", "owner_id": 1}
        create_resp = projects_client.post("/projects/", json=project_data)
        project_id = create_resp.json()["id"]

        response = projects_client.delete(f"/projects/{project_id}")
        assert response.status_code == 200

        response = projects_client.get(f"/projects/{project_id}")
        assert response.status_code == 404

    def test_get_projects_by_owner(self, projects_client):
        """Verifica que se pueden obtener proyectos por propietario."""
        projects_client.post("/projects/", json={"name": "Proj1", "owner_id": 42})
        projects_client.post("/projects/", json={"name": "Proj2", "owner_id": 42})

        response = projects_client.get("/projects/owner/42")
        assert response.status_code == 200
        assert len(response.json()) == 2


# ===================== TESTS DEL SERVICIO DE TAREAS =====================


class TestTasksService:
    """Pruebas para el microservicio de tareas."""

    def test_health_check(self, tasks_client):
        """Verifica que el servicio de tareas está activo."""
        response = tasks_client.get("/health")
        assert response.status_code == 200
        assert response.json()["service"] == "tasks"

    def test_create_task(self, tasks_client):
        """Verifica la creación de una nueva tarea."""
        task_data = {
            "title": "Tarea de Prueba",
            "description": "Descripción de la tarea",
            "project_id": 1,
            "status": "pendiente",
            "priority": "alta",
        }
        response = tasks_client.post("/tasks/", json=task_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Tarea de Prueba"
        assert data["status"] == "pendiente"
        assert data["priority"] == "alta"

    def test_list_tasks(self, tasks_client):
        """Verifica que se pueden listar las tareas."""
        response = tasks_client.get("/tasks/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_task_by_id(self, tasks_client):
        """Verifica que se puede obtener una tarea por su ID."""
        task_data = {"title": "Mi Tarea", "project_id": 1}
        create_resp = tasks_client.post("/tasks/", json=task_data)
        task_id = create_resp.json()["id"]

        response = tasks_client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "Mi Tarea"

    def test_get_task_not_found(self, tasks_client):
        """Verifica que se retorna 404 para una tarea inexistente."""
        response = tasks_client.get("/tasks/9999")
        assert response.status_code == 404

    def test_update_task(self, tasks_client):
        """Verifica la actualización de una tarea."""
        task_data = {"title": "Original", "project_id": 1}
        create_resp = tasks_client.post("/tasks/", json=task_data)
        task_id = create_resp.json()["id"]

        update_data = {"title": "Actualizada", "status": "en_progreso"}
        response = tasks_client.put(f"/tasks/{task_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["title"] == "Actualizada"
        assert response.json()["status"] == "en_progreso"

    def test_delete_task(self, tasks_client):
        """Verifica la eliminación de una tarea."""
        task_data = {"title": "Eliminar", "project_id": 1}
        create_resp = tasks_client.post("/tasks/", json=task_data)
        task_id = create_resp.json()["id"]

        response = tasks_client.delete(f"/tasks/{task_id}")
        assert response.status_code == 200

        response = tasks_client.get(f"/tasks/{task_id}")
        assert response.status_code == 404

    def test_get_tasks_by_project(self, tasks_client):
        """Verifica que se pueden obtener tareas por proyecto."""
        tasks_client.post("/tasks/", json={"title": "T1", "project_id": 10})
        tasks_client.post("/tasks/", json={"title": "T2", "project_id": 10})
        tasks_client.post("/tasks/", json={"title": "T3", "project_id": 20})

        response = tasks_client.get("/tasks/project/10")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_task_default_values(self, tasks_client):
        """Verifica los valores por defecto de una tarea."""
        task_data = {"title": "Defaults", "project_id": 1}
        response = tasks_client.post("/tasks/", json=task_data)
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "pendiente"
        assert data["priority"] == "media"
        assert data["assigned_to"] is None
