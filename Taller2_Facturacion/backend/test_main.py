import os
import sys
import pytest
from fastapi.testclient import TestClient
import importlib.util

# CARGA DINÁMICA: Forzamos la carga de main.py sin importar el PATH
current_dir = os.path.dirname(os.path.abspath(__file__))
main_path = os.path.join(current_dir, "main.py")

spec = importlib.util.spec_from_file_location("main", main_path)
main_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main_module)
app = main_module.app

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