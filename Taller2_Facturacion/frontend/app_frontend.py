$pathFrontend = "$PWD\Taller2_Facturacion\frontend\app_frontend.py"

$codeFrontend = @"
from flask import Flask, render_template, request, send_file
import requests
import io

app = Flask(__name__)

# URL del backend (usando el nombre del servicio en docker-compose)
BACKEND_URL = "http://backend:8000"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar', methods=['POST'])
def generar():
    # Recoger datos del formulario
    datos = {
        "numero_factura": request.form.get("numero"),
        "cliente_nombre": request.form.get("nombre"),
        "cliente_documento": request.form.get("documento"),
        "cliente_direccion": request.form.get("direccion"),
        "items": [
            {
                "descripcion": request.form.get("desc"),
                "cantidad": int(request.form.get("cant")),
                "precio_unitario": float(request.form.get("precio"))
            }
        ]
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/facturas/v1/generar", json=datos)
        if response.status_code == 200:
            return send_file(
                io.BytesIO(response.content),
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f"factura_{datos['numero_factura']}.pdf"
            )
        return f"Error en API Backend: {response.text}", 400
    except Exception as e:
        return f"Error de conexión: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
"@

[System.IO.File]::WriteAllText($pathFrontend, $codeFrontend, $utf8NoBom)
Write-Host "Archivo app_frontend.py creado con éxito." -ForegroundColor Green