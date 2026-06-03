import logging
import io
from faster_whisper import WhisperModel
from app.config.settings import settings

logger = logging.getLogger(__name__)


class STTService:
    def __init__(self):
        self.model = None

    def load_model(self):
        """Loads the whisper model into memory."""
        try:
            logger.info(
                f"Loading Whisper model '{settings.whisper_model}' on {settings.whisper_device}"
            )
            # compute_type "default" or "int8" for CPU, "float16" or "int8_float16" for GPU
            compute_type = "int8" if settings.whisper_device == "cpu" else "float16"
            self.model = WhisperModel(
                settings.whisper_model,
                device=settings.whisper_device,
                compute_type=compute_type,
            )
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            self.model = None

    def is_ready(self) -> bool:
        """Checks if the model is loaded and ready."""
        return self.model is not None

    def transcribe(self, audio_bytes: bytes, language: str = None) -> dict:
        """Transcribes audio bytes to text."""
        if not self.is_ready():
            raise RuntimeError("Model not loaded")

        logger.info("Starting transcription")
        # faster-whisper can read from a file-like object
        audio_stream = io.BytesIO(audio_bytes)

        try:
            kwargs = {}
            if language and language.lower() != "auto":
                kwargs["language"] = language

            segments, info = self.model.transcribe(audio_stream, beam_size=5, **kwargs)

            # segments is a generator, we need to consume it to get the text
            text = "".join(segment.text for segment in segments).strip()
            detected_language = info.language

            logger.info("Transcription completed")
            return {"text": text, "language": detected_language}
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise Exception("Transcription processing error") from e


# Create a global instance
stt_service = STTService()
