
import sys
from pathlib import Path

# Permite importar app.py desde la carpeta principal
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app


def test_cinco_estados():
    """
    Verifica que la función genere las cinco categorías.
    """
    casos = [
        (25, 36.5, 1, "NO ENFERMO"),
        (30, 37.8, 2, "ENFERMEDAD LEVE"),
        (70, 38.7, 2, "ENFERMEDAD AGUDA"),
        (45, 37.0, 40, "ENFERMEDAD CRÓNICA"),
        (70, 40.5, 35, "ENFERMEDAD TERMINAL"),
    ]

    for edad, temperatura, dias, esperado in casos:
        resultado = app.predecir_estado(
            edad, temperatura, dias
        )
        assert resultado == esperado, (
            f"Esperado: {esperado}, obtenido: {resultado}"
        )


def test_estadisticas(tmp_path, monkeypatch):
    """
    Verifica el registro y las estadísticas de predicciones.
    """

    # Aislar los datos de prueba
    monkeypatch.setattr(app, "DATA_DIR", tmp_path)
    monkeypatch.setattr(
        app,
        "ARCHIVO_PREDICCIONES",
        tmp_path / "predicciones.jsonl"
    )

    # Verificar estadísticas iniciales
    inicial = app.generar_estadisticas()

    assert all(
        total == 0
        for total in inicial["total_por_categoria"].values()
    )
    assert inicial["ultimas_5_predicciones"] == []
    assert inicial["fecha_ultima_prediccion"] is None

    # Generar siete predicciones simuladas
    casos = [
        (25, 36.5, 1),
        (30, 37.8, 2),
        (70, 38.7, 2),
        (45, 37.0, 40),
        (70, 40.5, 35),
        (25, 36.5, 1),
        (30, 37.8, 2)
    ]

    for edad, temperatura, dias in casos:
        estado = app.predecir_estado(
            edad, temperatura, dias
        )
        app.registrar_prediccion(estado)

    estadisticas = app.generar_estadisticas()
    totales = estadisticas["total_por_categoria"]

    # Verificar acumulación por categoría
    assert totales["NO ENFERMO"] == 2
    assert totales["ENFERMEDAD LEVE"] == 2
    assert totales["ENFERMEDAD AGUDA"] == 1
    assert totales["ENFERMEDAD CRÓNICA"] == 1
    assert totales["ENFERMEDAD TERMINAL"] == 1

    # Verificar únicamente las cinco últimas
    ultimas = estadisticas["ultimas_5_predicciones"]

    assert len(ultimas) == 5
    assert ultimas[0]["estado"] == "ENFERMEDAD LEVE"
    assert ultimas[-1]["estado"] == "ENFERMEDAD AGUDA"

    # Verificar fecha de última predicción
    assert estadisticas["fecha_ultima_prediccion"] is not None
    assert (
        estadisticas["fecha_ultima_prediccion"]
        == ultimas[0]["fecha"]
    )
