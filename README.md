# STT Service

Microservicio Speech-to-Text (STT) para arquitecturas de asistentes de voz.

## Descripción

STT Service es un microservicio encargado de convertir audio en texto utilizando Faster-Whisper.

Su única responsabilidad es recibir un archivo de audio mediante HTTP, procesarlo y devolver la transcripción resultante.

El servicio está diseñado para ejecutarse de forma independiente dentro de un contenedor Docker y formar parte de una arquitectura modular de asistentes de voz.

## Objetivos

* Recibir audio mediante HTTP.
* Convertir voz a texto utilizando Faster-Whisper.
* Devolver la transcripción al servicio llamante.
* Mantener una responsabilidad única y bien definida.
* Permitir despliegues independientes mediante Docker.
* Exponer una API simple, estable y fácilmente integrable.

## Fuera de alcance

Este servicio NO es responsable de:

* Captura de audio.
* Gestión de micrófonos.
* Voice Activity Detection (VAD).
* Gestión de contexto conversacional.
* Gestión de memoria.
* Ejecución de LLMs.
* Text-To-Speech (TTS).
* Orquestación de conversaciones.
* Integración con plugins o herramientas.
* Gestión de sesiones conversacionales.

## Arquitectura

Este servicio forma parte de una arquitectura más amplia:

```text
Usuario
   │
   ▼
Mic Daemon
   │
   │ POST audio
   ▼
STT Service
   │
   │ texto transcrito
   ▼
Interaction Manager / Orchestrator
   │
   ▼
LLM y herramientas
```

El STT Service únicamente se encarga de la transcripción.

## Principios de diseño

Este proyecto sigue los siguientes principios:

* Single Responsibility Principle (SRP).
* Separación clara de responsabilidades.
* Stateless API.
* Docker First.
* Infraestructura desacoplada.
* Configuración mediante variables de entorno.
* Componentes fácilmente testeables.
* Mínimas dependencias externas.

## Tecnologías utilizadas

* Python 3.12
* FastAPI
* Faster-Whisper
* Uvicorn
* Docker
* Docker Compose
* Pytest

## Requisitos previos

Para ejecutar el proyecto es necesario disponer de:

* Docker
* Docker Compose

No es necesario instalar Python localmente para ejecutar el servicio.

---

# Instalación

## Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd stt-capability
```

## Construir la imagen Docker

```bash
docker build -t stt-service .
```

## Ejecutar el servicio

```bash
docker run \
  -p 8000:8000 \
  -e WHISPER_MODEL=base \
  stt-service
```

El servicio quedará disponible en:

```text
http://localhost:8000
```

## Instalación mediante Docker Compose

```bash
docker compose up --build
```

Ejemplo de configuración:

```yaml
services:
  stt:
    build: .
    ports:
      - "8000:8000"
    environment:
      WHISPER_MODEL: base
      WHISPER_DEVICE: cpu
      LOG_LEVEL: INFO
      PORT: 8000
```

---

# Uso

## Health Check

```bash
curl http://localhost:8000/health
```

Respuesta:

```json
{
  "status": "ok"
}
```

## Readiness Check

```bash
curl http://localhost:8000/ready
```

Respuesta:

```json
{
  "status": "ready"
}
```

## Crear una transcripción

```bash
curl -X POST \
  -F "audio=@grabacion.wav" \
  -F "language=auto" \
  http://localhost:8000/v1/transcriptions
```

Respuesta:

```json
{
  "text": "qué tiempo hace hoy",
  "language": "es",
  "processing_ms": 842,
  "session_id": "abc123"
}
```

---

# API

## Endpoint principal

### POST /v1/transcriptions

Content-Type:

```text
multipart/form-data
```

### Parámetros

| Campo      | Obligatorio | Tipo   | Descripción                  |
| ---------- | ----------- | ------ | ---------------------------- |
| audio      | Sí          | File   | Archivo WAV                  |
| language   | No          | String | Idioma o auto                |
| session_id | No          | String | Identificador de correlación |

### Respuesta correcta

HTTP 200

```json
{
  "text": "qué tiempo hace hoy",
  "language": "es",
  "processing_ms": 842,
  "session_id": "abc123"
}
```

### Audio inválido

HTTP 400

```json
{
  "error": "invalid_audio"
}
```

### Error interno

HTTP 500

```json
{
  "error": "transcription_failed"
}
```

### Modelo no disponible

HTTP 503

```json
{
  "error": "model_unavailable"
}
```

---

# Configuración

La configuración se realiza mediante variables de entorno.

| Variable       | Valor por defecto | Descripción      |
| -------------- | ----------------- | ---------------- |
| WHISPER_MODEL  | base              | Modelo Whisper   |
| WHISPER_DEVICE | cpu               | CPU o GPU        |
| PORT           | 8000              | Puerto HTTP      |
| LOG_LEVEL      | INFO              | Nivel de logging |

## Modelos soportados

```text
tiny
base
small
medium
```

Ejemplo:

```bash
export WHISPER_MODEL=base
```

---

# Requisitos de implementación

Las siguientes restricciones forman parte del diseño oficial del servicio.

## Dockerización

La aplicación debe poder ejecutarse completamente dentro de Docker.

Docker es el mecanismo oficial de despliegue.

No se debe asumir:

* Acceso al sistema de archivos del host.
* Carpetas compartidas con otros servicios.
* Dependencias instaladas manualmente.

## Gestión del modelo Whisper

El modelo debe cargarse una única vez durante el arranque de la aplicación.

No debe cargarse en cada petición.

Implementación esperada:

```text
Startup
  └── Cargar modelo

Request
  └── Reutilizar modelo ya cargado
```

## Gestión de audio

El audio debe recibirse mediante HTTP.

No deben utilizarse rutas compartidas entre contenedores.

No deben intercambiarse nombres de archivos entre servicios.

El audio debe viajar como dato, no como referencia a disco.

## Gestión de errores

Todas las respuestas de error deben seguir el mismo formato:

```json
{
  "error": "<codigo>"
}
```

No deben devolverse trazas internas al cliente.

## Logging

Debe utilizarse el módulo estándar logging de Python.

No utilizar:

```python
print(...)
```

Debe registrarse:

* Inicio de la aplicación.
* Carga del modelo.
* Inicio de petición.
* Fin de petición.
* Tiempo de procesamiento.
* Errores.

No debe registrarse:

* Audio del usuario.
* Transcripciones completas.
* Datos sensibles.

---

# Estructura esperada del proyecto

```text
stt-capability/
├── app/
│   ├── api/
│   ├── services/
│   ├── config/
│   ├── models/
│   └── main.py
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── CONTRIBUTING.md
```

## Responsabilidades

### api/

Responsable de:

* Endpoints.
* Validación.
* Serialización.
* Respuestas HTTP.

### services/

Responsable de:

* Integración con Faster-Whisper.
* Lógica de transcripción.

### config/

Responsable de:

* Variables de entorno.
* Configuración global.

### models/

Responsable de:

* DTOs.
* Modelos de request y response.

---

# Testing

El proyecto debe incluir:

## Tests unitarios

Para:

* Servicios de transcripción.
* Configuración.
* Transformación de resultados.

## Tests de integración

Para:

* Endpoint /health
* Endpoint /ready
* Endpoint /v1/transcriptions

La ejecución de tests debe realizarse mediante:

```bash
pytest
```

---

# Desarrollo local

Ejecutar el servicio:

```bash
uvicorn app.main:app --reload
```

Ejecutar tests:

```bash
pytest
```

---

# Contribuciones

Las contribuciones son bienvenidas.

Antes de realizar cualquier contribución es obligatorio consultar:

```text
CONTRIBUTING.md
```

Este documento define:

* Convenciones de código.
* Arquitectura.
* Estándares de calidad.
* Estrategia de testing.
* Flujo de ramas.
* Revisión de cambios.
* Buenas prácticas de desarrollo.

Todo cambio deberá cumplir dichas directrices.

---

# Evolución futura

Posibles extensiones futuras:

* Streaming transcription.
* Resultados parciales.
* Confidence scores.
* Word timestamps.
* Voice Activity Detection (VAD).
* WebSockets.
* GPU acceleration.
* Multi-language optimization.

Estas funcionalidades quedan explícitamente fuera del alcance del MVP.

---

# Licencia

Pendiente de definir por el propietario del repositorio.
