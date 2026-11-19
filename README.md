# Sistema de Predicción de Enfermedades – MLOps

## Descripción del problema

Este proyecto aborda la necesidad de proporcionar a profesionales de la salud una herramienta que permita evaluar información básica de pacientes y obtener una clasificación simulada de su estado de salud.

La solución contempla inicialmente cuatro categorías: NO ENFERMO, ENFERMEDAD LEVE, ENFERMEDAD AGUDA y ENFERMEDAD CRÓNICA.

## Objetivo

Desarrollar y gestionar un servicio de predicción simulada mediante Flask y Docker, aplicando buenas prácticas de MLOps para el control de versiones, la integración continua y la automatización de pruebas y despliegues utilizando GitHub Actions.

## Estructura del repositorio

El proyecto se organizará con los siguientes componentes:

- `app.py`: aplicación Flask y lógica de predicción.
- `Dockerfile`: instrucciones para construir la imagen Docker.
- `requirements.txt`: dependencias de Python.
- `README.md`: documentación del proyecto.
- `tests/`: pruebas automatizadas de las funcionalidades.
- `.github/workflows/`: definición del pipeline de CI/CD.

## Tecnologías

Python, Flask, Docker, GitHub y GitHub Actions.

## Alcance

El proyecto utiliza una función basada en reglas para simular las predicciones, sin necesidad de entrenar un modelo real de Machine Learning. Su finalidad es académica y sus resultados no constituyen diagnósticos médicos.
