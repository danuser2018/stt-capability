import pytest
from unittest.mock import patch, MagicMock
from app.services.stt_service import STTService


@patch("app.services.stt_service.WhisperModel")
def test_stt_service_load_model_success(mock_whisper):
    mock_instance = MagicMock()
    mock_whisper.return_value = mock_instance

    service = STTService()
    assert not service.is_ready()

    service.load_model()

    assert service.is_ready()
    mock_whisper.assert_called_once()


@patch("app.services.stt_service.WhisperModel")
def test_stt_service_load_model_failure(mock_whisper):
    mock_whisper.side_effect = Exception("Download failed")

    service = STTService()
    service.load_model()

    assert not service.is_ready()
    assert service.model is None


def test_stt_service_transcribe_not_ready():
    service = STTService()

    with pytest.raises(RuntimeError, match="Model not loaded"):
        service.transcribe(b"dummy_data")


@patch("app.services.stt_service.WhisperModel")
def test_stt_service_transcribe_success(mock_whisper):
    # Setup mock
    mock_model = MagicMock()
    mock_segment = MagicMock()
    mock_segment.text = " hello world"
    mock_info = MagicMock()
    mock_info.language = "en"
    mock_model.transcribe.return_value = ([mock_segment], mock_info)

    mock_whisper.return_value = mock_model

    service = STTService()
    service.load_model()

    result = service.transcribe(b"dummy", language="en")

    assert result["text"] == "hello world"
    assert result["language"] == "en"
    mock_model.transcribe.assert_called_once()

    # Check that language keyword was passed
    _, kwargs = mock_model.transcribe.call_args
    assert kwargs.get("language") == "en"


@patch("app.services.stt_service.WhisperModel")
def test_stt_service_transcribe_auto_language(mock_whisper):
    mock_model = MagicMock()
    mock_segment = MagicMock()
    mock_segment.text = "test"
    mock_info = MagicMock()
    mock_info.language = "es"
    mock_model.transcribe.return_value = ([mock_segment], mock_info)

    mock_whisper.return_value = mock_model

    service = STTService()
    service.load_model()

    result = service.transcribe(b"dummy")

    assert result["text"] == "test"
    assert result["language"] == "es"

    # Check that language keyword was NOT passed when using default/auto
    _, kwargs = mock_model.transcribe.call_args
    assert "language" not in kwargs
