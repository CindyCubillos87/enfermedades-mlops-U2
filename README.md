# Servicio Docker para Predicción de Estado de Salud

## Descripción

Esta aplicación corresponde a una simulación académica de un sistema de apoyo a la decisión clínica. Recibe tres variables de entrada: edad, temperatura corporal y duración de síntomas, y genera uno de cuatro posibles estados:

- NO ENFERMO
- ENFERMEDAD LEVE
- ENFERMEDAD AGUDA
- ENFERMEDAD CRÓNICA

La función utiliza reglas predefinidas y no un modelo entrenado de Machine Learning, conforme a los requerimientos del ejercicio. Sus resultados son ficticios y no representan diagnósticos médicos.

## Requisitos

- Docker instalado y en ejecución.
- Puerto 5000 disponible.

## Construcción de la imagen Docker

Desde una terminal ubicada en la carpeta del proyecto, ejecutar:

`docker build -t mlops-enfermedades:1.0 .`

## Ejecución del contenedor

Ejecutar:

`docker run -d --name servicio-enfermedades -p 5000:5000 mlops-enfermedades:1.0`

## Uso de la aplicación

Abrir un navegador e ingresar a:

`http://localhost:5000`

Completar los campos de edad, temperatura corporal y días con síntomas. Seleccionar **Predecir** para visualizar el estado generado.

## Uso mediante API

El servicio también expone el endpoint:

`POST http://localhost:5000/predict`

Ejemplo de solicitud JSON:

```json
{
  "edad": 45,
  "temperatura": 39.5,
  "dias_sintomas": 2
}
```

Respuesta esperada:

```json
{
  "estado": "ENFERMEDAD AGUDA"
}
```

## Validación del servicio

Consultar:

`http://localhost:5000/health`

Respuesta esperada: `{"status":"OK"}`.

## Detener y eliminar el contenedor

`docker stop servicio-enfermedades`

`docker rm servicio-enfermedades`

## Consideraciones

Esta solución demuestra el empaquetado y despliegue de un servicio predictivo simulado mediante una imagen personalizada de Docker. No constituye un dispositivo médico ni debe emplearse para diagnóstico o tratamiento real.
