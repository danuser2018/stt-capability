import time
import logging
import struct
from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import JSONResponse
from typing import Optional

from app.models.schemas import (
    HealthResponse,
    ReadyResponse,
    TranscriptionResponse,
    ErrorResponse,
)
from app.services.stt_service import stt_service

logger = logging.getLogger(__name__)

router = APIRouter()


def validate_wav_header(audio_bytes: bytes) -> bool:
    """Validates that the WAV file has the expected format: PCM 16-bit Mono at 16000 Hz."""
    if len(audio_bytes) < 44:
        return False
    if audio_bytes[0:4] != b"RIFF" or audio_bytes[8:12] != b"WAVE":
        return False
    if audio_bytes[12:16] != b"fmt ":
        return False
    try:
        audio_format, num_channels, sample_rate = struct.unpack("<HHI", audio_bytes[20:28])
        bits_per_sample = struct.unpack("<H", audio_bytes[34:36])[0]
        return audio_format == 1 and num_channels == 1 and sample_rate == 16000 and bits_per_sample == 16
    except Exception:
        return False


@router.get("/health", response_model=HealthResponse)
def health_check():
    return {"status": "ok"}


@router.get("/ready", response_model=ReadyResponse)
def ready_check():
    if not stt_service.is_ready():
        return JSONResponse(status_code=503, content={"error": "model_unavailable"})
    return {"status": "ready"}


@router.post(
    "/v1/transcriptions",
    response_model=TranscriptionResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
        503: {"model": ErrorResponse},
    },
)
async def transcribe_audio(
    audio: UploadFile = File(...),
    language: Optional[str] = Form("auto"),
    session_id: Optional[str] = Form(None),
):
    start_time = time.time()
    logger.info(f"Received transcription request, session_id: {session_id}")

    if not stt_service.is_ready():
        logger.error("Model unavailable")
        return JSONResponse(status_code=503, content={"error": "model_unavailable"})

    # Validate audio
    if not audio.filename.endswith(".wav"):
        logger.warning(f"Invalid audio format for file: {audio.filename}")
        return JSONResponse(status_code=400, content={"error": "invalid_audio"})

    try:
        audio_bytes = await audio.read()
        if not audio_bytes:
            processing_ms = int((time.time() - start_time) * 1000)
            logger.info(f"Empty audio file received, returning empty transcription. session_id: {session_id}")
            return TranscriptionResponse(
                text="",
                language=language or "auto",
                processing_ms=processing_ms,
                session_id=session_id,
            )

        # Validate WAV format consistency (PCM 16-bit Mono at 16000 Hz)
        if not validate_wav_header(audio_bytes):
            logger.warning("Audio header does not match expected format (16kHz, mono, 16-bit PCM WAV)")
            return JSONResponse(status_code=400, content={"error": "invalid_audio"})

        result = stt_service.transcribe(audio_bytes, language)

        processing_ms = int((time.time() - start_time) * 1000)
        logger.info(f"Request completed in {processing_ms}ms, session_id: {session_id}")

        return TranscriptionResponse(
            text=result["text"],
            language=result["language"],
            processing_ms=processing_ms,
            session_id=session_id,
        )
    except RuntimeError as e:
        logger.error(f"Runtime error during transcription: {e}")
        return JSONResponse(status_code=503, content={"error": "model_unavailable"})
    except Exception as e:
        if str(e) == "Transcription processing error":
            logger.warning(f"Invalid audio format or decoding failed: {e}")
            return JSONResponse(status_code=400, content={"error": "invalid_audio"})
        logger.error(f"Error during transcription: {e}")
        return JSONResponse(status_code=500, content={"error": "transcription_failed"})
