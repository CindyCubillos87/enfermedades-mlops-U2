

from flask import Flask, request, jsonify, render_template_string
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter
from threading import Lock
import json

app = Flask(__name__)

# ====================================================
# CONFIGURACIÓN DEL REGISTRO DE PREDICCIONES
# ====================================================

DATA_DIR = Path(__file__).resolve().parent / "data"
ARCHIVO_PREDICCIONES = DATA_DIR / "predicciones.jsonl"
LOCK = Lock()

CATEGORIAS = [
    "NO ENFERMO",
    "ENFERMEDAD LEVE",
    "ENFERMEDAD AGUDA",
    "ENFERMEDAD CRÓNICA",
    "ENFERMEDAD TERMINAL"
]


# ====================================================
# FUNCIÓN DE PREDICCIÓN SIMULADA
# ====================================================

def predecir_estado(edad, temperatura, dias_sintomas):
    """
    Simulación académica.
    No representa criterios de diagnóstico médico.
    """

    if edad >= 65 and temperatura >= 40 and dias_sintomas >= 30:
        return "ENFERMEDAD TERMINAL"

    elif dias_sintomas >= 30:
        return "ENFERMEDAD CRÓNICA"

    elif temperatura >= 39 or (edad >= 65 and temperatura >= 38.5):
        return "ENFERMEDAD AGUDA"

    elif temperatura >= 37.5 or dias_sintomas >= 3:
        return "ENFERMEDAD LEVE"

    else:
        return "NO ENFERMO"


# ====================================================
# NUEVO: REGISTRAR PREDICCIONES
# ====================================================

def registrar_prediccion(estado):
    """
    Guarda cada predicción con fecha y hora UTC.
    """

    registro = {
        "estado": estado,
        "fecha": datetime.now(timezone.utc).isoformat()
    }

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with LOCK:
        with open(
            ARCHIVO_PREDICCIONES, "a", encoding="utf-8"
        ) as archivo:
            archivo.write(
                json.dumps(registro, ensure_ascii=False) + "\n"
            )


# ====================================================
# NUEVO: GENERAR ESTADÍSTICAS
# ====================================================

def generar_estadisticas():
    """
    Calcula totales por categoría, últimas cinco
    predicciones y fecha de la última predicción.
    """

    registros = []

    with LOCK:
        if ARCHIVO_PREDICCIONES.exists():
            with open(
                ARCHIVO_PREDICCIONES, "r", encoding="utf-8"
            ) as archivo:
                for linea in archivo:
                    if linea.strip():
                        registros.append(json.loads(linea))

    conteo = Counter(
        registro["estado"] for registro in registros
    )

    total_por_categoria = {
        categoria: conteo.get(categoria, 0)
        for categoria in CATEGORIAS
    }

    ultimas_cinco = list(reversed(registros[-5:]))

    fecha_ultima = (
        registros[-1]["fecha"] if registros else None
    )

    return {
        "total_por_categoria": total_por_categoria,
        "ultimas_5_predicciones": ultimas_cinco,
        "fecha_ultima_prediccion": fecha_ultima
    }


# ====================================================
# INTERFAZ WEB ORIGINAL
# ====================================================

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Predicción de Estado de Salud</title>
</head>
<body>
    <h2>Sistema de Predicción de Estado de Salud</h2>
    <p>Demostración académica, no apta para diagnóstico.</p>

    <form method="POST" action="/">
        <label>Edad:</label>
        <input type="number" name="edad" min="0" max="120"
               required><br><br>

        <label>Temperatura (°C):</label>
        <input type="number" name="temperatura"
               min="30" max="45" step="0.1"
               required><br><br>

        <label>Días con síntomas:</label>
        <input type="number" name="dias_sintomas"
               min="0" max="3650" required><br><br>

        <button type="submit">Predecir</button>
    </form>

    {% if resultado %}
    <h3>Resultado: {{ resultado }}</h3>
    {% endif %}

    {% if error %}
    <p style="color:red">{{ error }}</p>
    {% endif %}

    <p><a href="/statistics">Consultar estadísticas</a></p>
</body>
</html>
"""


# ====================================================
# VALIDACIÓN DE DATOS ORIGINAL
# ====================================================

def validar_datos(datos):
    edad = int(datos["edad"])
    temperatura = float(datos["temperatura"])
    dias = int(datos["dias_sintomas"])

    if not (0 <= edad <= 120):
        raise ValueError("Edad fuera de rango")
    if not (30 <= temperatura <= 45):
        raise ValueError("Temperatura fuera de rango")
    if not (0 <= dias <= 3650):
        raise ValueError("Días fuera de rango")

    return edad, temperatura, dias


# ====================================================
# FORMULARIO WEB
# ====================================================

@app.route("/", methods=["GET", "POST"])
def home():
    resultado = None
    error = None

    if request.method == "POST":
        try:
            edad, temperatura, dias = validar_datos(request.form)
            resultado = predecir_estado(edad, temperatura, dias)

            # NUEVO: registrar la predicción
            registrar_prediccion(resultado)

        except (ValueError, KeyError, TypeError):
            error = "Ingrese valores válidos."

    return render_template_string(
        HTML, resultado=resultado, error=error
    )


# ====================================================
# HEALTH CHECK
# ====================================================

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "OK"})


# ====================================================
# API DE PREDICCIÓN
# ====================================================

@app.route("/predict", methods=["POST"])
def predict():
    try:
        edad, temperatura, dias = validar_datos(
            request.get_json(silent=True) or {}
        )

        estado = predecir_estado(edad, temperatura, dias)

        # NUEVO: registrar la predicción
        registrar_prediccion(estado)

        return jsonify({"estado": estado})

    except (ValueError, KeyError, TypeError):
        return jsonify({"error": "Datos inválidos"}), 400


# ====================================================
# NUEVO: API DE ESTADÍSTICAS
# ====================================================

@app.route("/statistics", methods=["GET"])
def statistics():
    return jsonify(generar_estadisticas())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


