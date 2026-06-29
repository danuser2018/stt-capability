# Registro de cambios

Todos los cambios notables de este proyecto se documentan en este fichero.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y este proyecto adhiere a [Versionado Semántico](https://semver.org/lang/es/).

## Guía de uso

Cada versión se documenta bajo su número de versión y fecha de publicación.
Los cambios se agrupan en las siguientes categorías:

- **Añadido** — nuevas funcionalidades.
- **Cambiado** — cambios en funcionalidades existentes.
- **Obsoleto** — funcionalidades que serán eliminadas en versiones futuras.
- **Eliminado** — funcionalidades eliminadas en esta versión.
- **Corregido** — corrección de errores.
- **Seguridad** — correcciones de vulnerabilidades.

---

## Sin publicar

### Añadido

- Test de integración `test_transcribe_audio_invalid_wav_format` para verificar el rechazo de audios con formato físico incorrecto.

### Corregido

- Validación del formato físico del audio recibido (PCM 16-bit, Mono a 16000 Hz) antes de procesar la transcripción, de acuerdo con la invariante de la Skill `inference-subsystem`.

## [1.2.0] - 2026-06-29

### Añadido

- Carpeta `.agent/skills` creada con información para desarrollo por IA.
- Tests unitarios y de integración para validar el comportamiento con audios vacíos y errores de procesamiento.

### Corregido

- Manejo de archivos de audio vacíos (0 bytes) para que retornen una transcripción vacía controlada (HTTP 200) en lugar de un error HTTP 400.
- Respuestas HTTP ante errores de decodificación de audio, retornando ahora HTTP 400 (`invalid_audio`) en lugar de HTTP 500 (`transcription_failed`).
- Referencias erróneas al ecosistema Node/JS (Jest, npm) y al servicio `tts` en `CONTRIBUTING.md` y `CHANGELOG.md`.
- Nombres del directorio de instalación del proyecto en `README.md` para coincidir con `stt-capability`.
- Ejemplo de configuración de Docker Compose en `README.md` para incluir `LOG_LEVEL` y `PORT`.

## [1.1.0] - 2026-06-14

### Corregido

- Se añade la variable de entorno `HF_HUB_DISABLE_XET` con valor 1 al archivo Dockerfile, para evitar un problema con la descarga del modelo.

## [1.0.0] - 2026-06-03

### Añadido

- Fichero `CONTRIBUTING.md` con el flujo de trabajo Trunk Based Development,
  convenciones de commits, guía de Pull Requests y buenas prácticas para
  desarrollo asistido con IA.
- Fichero `CHANGELOG.md` con el formato Keep a Changelog v1.1.0 en castellano.
- Implementación completa del servicio STT utilizando FastAPI y Faster-Whisper.
- Soporte para despliegue aislado mediante `Dockerfile` y `docker-compose.yml`.
- Configuración de tests unitarios y de integración con `pytest` y dependencias simuladas (mocks).
- Pipeline de CI con GitHub Actions (`.github/workflows/ci.yml`) para verificar automáticamente los tests y linting (black, flake8) en las Pull Requests.

---

<!-- Plantilla para nuevas versiones:

## [X.Y.Z] - AAAA-MM-DD

### Añadido
-

### Cambiado
-

### Obsoleto
-

### Eliminado
-

### Corregido
-

### Seguridad
-

-->

[Sin publicar]: https://github.com/danuser2018/stt-capability/compare/HEAD...HEAD
