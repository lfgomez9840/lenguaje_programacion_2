from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = FastAPI(title="API de Facturación v1")


class Item(BaseModel):
    descripcion: str
    cantidad: int
    precio_unitario: float


class Factura(BaseModel):
    numero_factura: str
    cliente_nombre: str
    cliente_documento: str
    cliente_direccion: str
    items: List[Item]


OS_PATH = os.path.dirname(os.path.abspath(__file__))
FACTURAS_DIR = os.path.join(OS_PATH, "archivos_facturas")
os.makedirs(FACTURAS_DIR, exist_ok=True)


@app.get("/")
async def root():
    return {"message": "API de Facturación v1 activa"}


@app.post("/facturas/v1/generar")
async def generar_factura(factura: Factura):
    file_path = os.path.join(FACTURAS_DIR, f"{factura.numero_factura}.pdf")
    try:
        c = canvas.Canvas(file_path, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 750, f"FACTURA: {factura.numero_factura}")
        c.setFont("Helvetica", 12)
        c.drawString(100, 730, f"Cliente: {factura.cliente_nombre}")
        c.drawString(100, 715, f"Documento: {factura.cliente_documento}")
        c.drawString(100, 700, f"Dirección: {factura.cliente_direccion}")
        y = 660
        c.drawString(100, y, "Cant. | Descripción | Precio Unit. | Total")
        c.line(100, y - 5, 500, y - 5)
        total_general = 0
        y -= 25
        for item in factura.items:
            total_item = item.cantidad * item.precio_unitario
            total_general += total_item
            c.drawString(
                100,
                y,
                f"{item.cantidad} | {item.descripcion} | ${item.precio_unitario} | ${total_item}",
            )
            y -= 20
        c.line(100, y, 500, y)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y - 20, f"TOTAL A PAGAR: ${total_general}")
        c.save()
        return FileResponse(
            path=file_path,
            filename=f"{factura.numero_factura}.pdf",
            media_type="application/pdf",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/facturas/v1/{numero_factura}")
async def obtener_factura(numero_factura: str):
    file_path = os.path.join(FACTURAS_DIR, f"{numero_factura}.pdf")
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename=f"{numero_factura}.pdf",
            media_type="application/pdf",
        )
    try:
        c = canvas.Canvas(file_path, pagesize=letter)
        c.drawString(100, 750, f"FACTURA DE PRUEBA: {numero_factura}")
        c.save()
        return FileResponse(
            path=file_path,
            filename=f"{numero_factura}.pdf",
            media_type="application/pdf",
        )
    except Exception:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
