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

## Sin publicar

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

[Sin publicar]: https://github.com/danuser2018/tts-capability/compare/HEAD...HEAD
