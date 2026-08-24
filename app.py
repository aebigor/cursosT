"""
Centros de Formación en Empresa - Ministerio del Trabajo
Réplica de la página de consulta, ahora respaldada por una base de datos SQLite.
"""
from flask import Flask, render_template, request, redirect, url_for

from database import init_db, buscar_persona, sembrar_personas
from personas_data import PERSONAS

app = Flask(__name__)
app.secret_key = "cambia-esta-clave-en-produccion"  # usa variable de entorno en prod

TIPOS_DOCUMENTO = [
    ("", "Seleccione"),
    ("CC", "Cédula de Ciudadanía"),
    ("CE", "Cédula de Extranjería"),
    ("TI", "Tarjeta de Identidad"),
    ("PA", "Pasaporte"),
    ("PEP", "Permiso Especial de Permanencia"),
]

# Se ejecuta en cada arranque de la app (local o en Render):
# crea las tablas si no existen y registra/actualiza a PERSONAS desde
# personas_data.py. Por eso no hace falta correr ningún script aparte.
init_db()
sembrar_personas(PERSONAS)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", tipos_documento=TIPOS_DOCUMENTO)


@app.route("/consultar", methods=["POST"])
def consultar():
    tipo_doc = request.form.get("tipo_documento", "")
    numero_doc = request.form.get("numero_documento", "").strip()

    if not tipo_doc or not numero_doc:
        return redirect(url_for("index"))

    resultado = buscar_persona(tipo_doc, numero_doc)

    return render_template(
        "resultado.html",
        resultado=resultado,
        tipo_doc=tipo_doc,
        numero_doc=numero_doc,
    )


if __name__ == "__main__":
    app.run(debug=True)
