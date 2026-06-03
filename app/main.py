import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.services.stt_service import stt_service
from app.config.settings import settings

# Setup standard logging
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up application...")
    # Load the Whisper model on startup
    stt_service.load_model()
    yield
    logger.info("Shutting down application...")


app = FastAPI(
    title="STT Service",
    description="Microservicio Speech-to-Text (STT) utilizando Faster-Whisper",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api_router)
