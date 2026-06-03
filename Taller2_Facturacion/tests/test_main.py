from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_obtener_factura():
    response = client.get("/facturas/v1/TEST-001")
    assert response.status_code == 200
    data = response.json()
    assert data["numero_factura"] == "TEST-001"
    assert "items" in data
    assert len(data["items"]) == 2


def test_generar_factura():
    payload = {
        "numero_factura": "FAC-001",
        "cliente_nombre": "Juan Pérez",
        "cliente_documento": "123456789",
        "cliente_direccion": "Calle 123, Bogotá",
        "items": [
            {"descripcion": "Laptop", "cantidad": 1, "precio_unitario": 2500000.0},
            {"descripcion": "Mouse", "cantidad": 2, "precio_unitario": 85000.0},
        ],
    }
    response = client.post("/facturas/v1/generar", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "pdf_base64" in data
    assert data["numero_factura"] == "FAC-001"