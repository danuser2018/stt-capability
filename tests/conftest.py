import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient


# Mock the STTService to avoid loading the actual model
@pytest.fixture(autouse=True)
def mock_stt_service():
    with patch("app.api.endpoints.stt_service") as mock_api_service, patch(
        "app.main.stt_service"
    ) as _mock_main_service:  # noqa: F841

        # Configure the mock
        mock_api_service.is_ready.return_value = True
        mock_api_service.transcribe.return_value = {
            "text": "test transcription",
            "language": "es",
        }

        # We need to make sure the main.py uses the mocked service too
        yield mock_api_service


@pytest.fixture
def client():
    # Import inside the fixture to ensure mocks are applied first
    from app.main import app

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def dummy_wav_file():
    # A valid but empty/dummy WAV header
    return b"RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00D\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00"
