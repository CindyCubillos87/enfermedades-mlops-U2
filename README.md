# Servicio Docker para Predicción de Estado de Salud
Cindy Cubillos y Maria jose caicedo
## 1. Descripción del proyecto

Este proyecto implementa un servicio web de predicción simulada del estado de salud de pacientes, desarrollado en Python con Flask y desplegado mediante una imagen personalizada de Docker.

La aplicación permite ingresar tres variables clínicas y obtener uno de cinco posibles estados:

- NO ENFERMO
- ENFERMEDAD LEVE
- ENFERMEDAD AGUDA
- ENFERMEDAD CRÓNICA
- ENFERMEDAD TERMINAL

Adicionalmente, el sistema registra las predicciones realizadas y permite consultar estadísticas de su utilización.

Para este ejercicio no se utiliza un modelo de Machine Learning entrenado. Se implementa una función de clasificación mediante reglas predefinidas.

**Nota:** La clasificación es exclusivamente una simulación académica. No representa un diagnóstico médico ni debe utilizarse para tomar decisiones clínicas.

## 2. Estructura del proyecto

```text
enfermedades-mlops-U2/
│
├── app.py
├── Dockerfile
├── requirements.txt
├── README.md
└── data/
    └── predicciones.jsonl  (generado automáticamente)
```

**Descripción de los archivos:**

- `app.py`: aplicación Flask, función de clasificación simulada, validación de datos, registro de predicciones y endpoints.
- `Dockerfile`: instrucciones para construir la imagen Docker.
- `requirements.txt`: dependencias necesarias para ejecutar la aplicación.
- `README.md`: documentación de instalación, ejecución y uso.
- `data/predicciones.jsonl`: archivo generado automáticamente para almacenar el historial de predicciones.

## 3. Funcionamiento de la aplicación

El servicio recibe tres variables:

| Variable | Descripción |
|---|---|
| edad | Edad del paciente en años |
| temperatura | Temperatura corporal en grados Celsius |
| dias_sintomas | Número de días con síntomas |

La función `predecir_estado()` utiliza reglas condicionales para asignar una de las cinco categorías.

Los resultados pueden obtenerse mediante un formulario web o mediante una API REST.

Cada predicción válida se registra automáticamente con su categoría y fecha de ejecución en formato UTC, permitiendo generar estadísticas del uso del sistema.

## 4. Requisitos previos

Para ejecutar la aplicación mediante Docker se requiere:

- Docker Desktop instalado y en funcionamiento, o Docker Engine en un entorno compatible.
- Acceso a una terminal de comandos.
- Puerto 5000 disponible.

No se requiere instalar Python localmente, ya que la imagen Docker contiene el entorno y las dependencias necesarias.

## 5. Construcción de la imagen Docker

Ubicarse en el directorio que contiene el `Dockerfile` y ejecutar:

```bash
docker build -t mlops-enfermedades:2.0 .
```

Este comando construye la imagen Docker utilizando el código actualizado de la aplicación.

Para verificar que la imagen se haya construido:

```bash
docker images
```

## 6. Ejecución del contenedor

Ejecutar el siguiente comando en una sola línea:

```bash
docker run -d --name servicio-enfermedades -p 5000:5000 -v predicciones_data:/app/data mlops-enfermedades:2.0
```

El parámetro `-p 5000:5000` conecta el puerto del computador con el puerto del contenedor.

El parámetro `-v predicciones_data:/app/data` configura un volumen persistente para conservar las predicciones registradas cuando el contenedor sea eliminado o reemplazado.

Para comprobar que el contenedor está ejecutándose:

```bash
docker ps
```

## 7. Uso de la interfaz web

Abrir un navegador e ingresar a:

http://localhost:5000

El formulario permite introducir edad, temperatura y días con síntomas. Al seleccionar **Predecir**, la aplicación muestra el estado simulado y registra automáticamente el resultado.

### Casos de prueba

| Edad | Temperatura | Días | Resultado esperado |
|---|---|---|---|
| 25 | 36.5 | 1 | NO ENFERMO |
| 30 | 37.8 | 2 | ENFERMEDAD LEVE |
| 70 | 38.7 | 2 | ENFERMEDAD AGUDA |
| 45 | 37.0 | 40 | ENFERMEDAD CRÓNICA |
| 70 | 40.5 | 35 | ENFERMEDAD TERMINAL |

## 8. API REST de predicción

La aplicación expone el endpoint:

`POST http://localhost:5000/predict`

Ejemplo de solicitud:

```json
{
  "edad": 70,
  "temperatura": 40.5,
  "dias_sintomas": 35
}
```

Respuesta esperada:

```json
{
  "estado": "ENFERMEDAD TERMINAL"
}
```

Cada solicitud válida también genera un registro en el historial de predicciones.

## 9. Consulta de estadísticas

El sistema incorpora un endpoint para consultar las estadísticas acumuladas:

`GET http://localhost:5000/statistics`

Este endpoint retorna:

1. **Total por categoría:** cantidad de predicciones realizadas para cada uno de los cinco estados.
2. **Últimas cinco predicciones:** registros más recientes, incluyendo la categoría y fecha.
3. **Fecha de la última predicción:** marca de tiempo de la consulta más reciente.

Ejemplo ilustrativo de respuesta:

```json
{
  "total_por_categoria": {
    "NO ENFERMO": 2,
    "ENFERMEDAD LEVE": 2,
    "ENFERMEDAD AGUDA": 1,
    "ENFERMEDAD CRÓNICA": 1,
    "ENFERMEDAD TERMINAL": 1
  },
  "ultimas_5_predicciones": [
    {
      "estado": "ENFERMEDAD LEVE",
      "fecha": "2026-11-19T23:13:49+00:00"
    }
  ],
  "fecha_ultima_prediccion": "2026-11-19T23:13:49+00:00"
}
```

Este ejemplo muestra la estructura de los datos; en una consulta real, el campo `ultimas_5_predicciones` contiene hasta cinco registros, ordenados del más reciente al más antiguo.

Si todavía no existen predicciones, los conteos serán cero, la lista estará vacía y la fecha será `null`.

El archivo JSONL utilizado para almacenar los registros se crea automáticamente cuando se genera la primera predicción.

## 10. Verificación del servicio

Para comprobar que la aplicación está disponible, acceder a:

`GET http://localhost:5000/health`

Respuesta:

```json
{
  "status": "OK"
}
```

También se pueden consultar los logs del contenedor:

```bash
docker logs servicio-enfermedades
```

## 11. Administración del contenedor

Detener el servicio:

```bash
docker stop servicio-enfermedades
```

Iniciarlo nuevamente:

```bash
docker start servicio-enfermedades
```

Eliminar el contenedor después de detenerlo:

```bash
docker rm servicio-enfermedades
```

El volumen `predicciones_data` permite conservar los registros de predicción independientemente del ciclo de vida del contenedor, siempre que se reutilice el mismo volumen.

## 12. Pruebas realizadas

La función de clasificación y el módulo de estadísticas fueron probados mediante Google Colab utilizando el código de la rama `feature/estadisticas`.

Se verificó que:

- La función puede generar las cinco categorías de clasificación.
- Las estadísticas iniciales estén vacías antes de realizar predicciones.
- Las predicciones se registren y acumulen correctamente.
- Se obtengan los totales por categoría.
- Se recuperen únicamente las últimas cinco predicciones.
- Se genere correctamente la fecha de la última predicción.

Las pruebas funcionales de Python fueron satisfactorias. La validación automatizada de los endpoints y la construcción de la imagen Docker forman parte de la siguiente etapa de CI/CD.

## 13. Conclusión

La solución permite simular un servicio predictivo mediante Flask y Docker, incorporando cinco estados de salud y un mecanismo de registro y consulta de estadísticas.

Esta implementación constituye la base para aplicar prácticas de integración y entrega continua mediante GitHub Actions, automatizando las pruebas y la construcción de imágenes Docker en las siguientes etapas del proyecto.
