from flask import Flask, render_template, request, jsonify, send_file
import requests
import io
import base64

app = Flask(__name__)

BACKEND_URL = "http://backend:8000"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generar-factura", methods=["POST"])
def generar_factura():
    data = request.get_json()

    items = []
    for item in data.get("items", []):
        items.append({
            "descripcion": item["descripcion"],
            "cantidad": int(item["cantidad"]),
            "precio_unitario": float(item["precio_unitario"])
        })

    payload = {
        "numero_factura": data["numero_factura"],
        "cliente_nombre": data["cliente_nombre"],
        "cliente_documento": data["cliente_documento"],
        "cliente_direccion": data["cliente_direccion"],
        "items": items
    }

    try:
        response = requests.post(f"{BACKEND_URL}/facturas/v1/generar", json=payload)
        response.raise_for_status()
        resultado = response.json()

        pdf_bytes = base64.b64decode(resultado["pdf_base64"])
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"factura_{resultado['numero_factura']}.pdf"
        )
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)