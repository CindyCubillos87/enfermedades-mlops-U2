
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

def predecir_estado(edad, temperatura, dias_sintomas):
    # Simulación académica, no diagnóstico médico
    if dias_sintomas >= 30:
        return "ENFERMEDAD CRÓNICA"
    elif temperatura >= 39 or (edad >= 65 and temperatura >= 38.5):
        return "ENFERMEDAD AGUDA"
    elif temperatura >= 37.5 or dias_sintomas >= 3:
        return "ENFERMEDAD LEVE"
    else:
        return "NO ENFERMO"


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
               min="30" max="45" step="0.1" required><br><br>
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
</body>
</html>
"""


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


@app.route("/", methods=["GET", "POST"])
def home():
    resultado = None
    error = None

    if request.method == "POST":
        try:
            edad, temperatura, dias = validar_datos(request.form)
            resultado = predecir_estado(edad, temperatura, dias)
        except (ValueError, KeyError, TypeError):
            error = "Ingrese valores válidos."

    return render_template_string(
        HTML, resultado=resultado, error=error
    )


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "OK"})


@app.route("/predict", methods=["POST"])
def predict():
    try:
        edad, temperatura, dias = validar_datos(
            request.get_json(silent=True) or {}
        )
        estado = predecir_estado(edad, temperatura, dias)
        return jsonify({"estado": estado})
    except (ValueError, KeyError, TypeError):
        return jsonify({"error": "Datos inválidos"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

