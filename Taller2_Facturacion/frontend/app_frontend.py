from flask import Flask, render_template, request, Response
import requests
import os

app = Flask(__name__)
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generar", methods=["POST"])
def generar():
    try:
        data = request.json
        response = requests.post(
            f"{BACKEND_URL}/facturas/v1/generar", json=data, timeout=10
        )
        if response.status_code == 200:
            return Response(
                response.content,
                mimetype="application/pdf",
                headers={
                    "Content-disposition": f"attachment; filename=factura_{data.get('numero_factura', '001')}.pdf"
                },
            )
        return {"error": "El backend devolvió un error"}, response.status_code
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
