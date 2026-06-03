def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ready_check(client):
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_ready_check_unavailable(client, mock_stt_service):
    mock_stt_service.is_ready.return_value = False
    response = client.get("/ready")
    assert response.status_code == 503
    assert response.json() == {"error": "model_unavailable"}


def test_transcribe_audio_success(client, dummy_wav_file):
    files = {"audio": ("test.wav", dummy_wav_file, "audio/wav")}
    data = {"language": "es", "session_id": "test_session"}

    response = client.post("/v1/transcriptions", files=files, data=data)

    assert response.status_code == 200
    res_data = response.json()
    assert res_data["text"] == "test transcription"
    assert res_data["language"] == "es"
    assert "processing_ms" in res_data
    assert res_data["session_id"] == "test_session"


def test_transcribe_audio_invalid_file_extension(client, dummy_wav_file):
    files = {"audio": ("test.mp3", dummy_wav_file, "audio/mp3")}

    response = client.post("/v1/transcriptions", files=files)

    assert response.status_code == 400
    assert response.json() == {"error": "invalid_audio"}


def test_transcribe_model_unavailable(client, mock_stt_service, dummy_wav_file):
    mock_stt_service.is_ready.return_value = False
    files = {"audio": ("test.wav", dummy_wav_file, "audio/wav")}

    response = client.post("/v1/transcriptions", files=files)

    assert response.status_code == 503
    assert response.json() == {"error": "model_unavailable"}


def test_transcribe_runtime_error(client, mock_stt_service, dummy_wav_file):
    mock_stt_service.transcribe.side_effect = Exception("Some internal error")
    files = {"audio": ("test.wav", dummy_wav_file, "audio/wav")}

    response = client.post("/v1/transcriptions", files=files)

    assert response.status_code == 500
    assert response.json() == {"error": "transcription_failed"}
