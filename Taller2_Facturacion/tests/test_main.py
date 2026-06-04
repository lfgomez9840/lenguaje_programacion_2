import os
import sys
import pytest
from fastapi.testclient import TestClient

# Añadimos la carpeta padre a la ruta de búsqueda
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ahora importamos 'main' que está en la carpeta 'backend'
from backend.main import app # noqa: E402

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API de Facturación v1 activa"}

def test_obtener_factura():
    response = client.get("/facturas/v1/TEST-001")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"

def test_generar_factura():
    payload = {
        "numero_factura": "FAC-001",
        "cliente_nombre": "Luis Felipe",
        "cliente_documento": "12345",
        "cliente_direccion": "Calle Falsa",
        "items": [{"descripcion": "Test", "cantidad": 1, "precio_unitario": 10.0}]
    }
    response = client.post("/facturas/v1/generar", json=payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"