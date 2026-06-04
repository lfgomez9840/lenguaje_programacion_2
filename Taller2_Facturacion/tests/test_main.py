import os
import sys

# Forzamos a Python a encontrar la carpeta raíz del Taller
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import pytest
from fastapi.testclient import TestClient

# Ahora la importación será segura
try:
    from backend.main import app
except ImportError:
    from main import app # Fallback si ya está en la raíz

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
        "cliente_documento": "123456",
        "cliente_direccion": "Calle 123",
        "items": [{"descripcion": "Test", "cantidad": 1, "precio_unitario": 10.0}]
    }
    response = client.post("/facturas/v1/generar", json=payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"