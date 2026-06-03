from pydantic import BaseModel
from typing import Optional


class HealthResponse(BaseModel):
    status: str


class ReadyResponse(BaseModel):
    status: str


class TranscriptionResponse(BaseModel):
    text: str
    language: str
    processing_ms: int
    session_id: Optional[str] = None


class ErrorResponse(BaseModel):
    error: str
