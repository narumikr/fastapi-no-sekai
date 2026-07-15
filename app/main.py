import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.adapter.controllers.artist_controller import router as artist_router
from app.adapter.infrastructure.db.base_entity import Base
from app.core.database import engine
from app.core.global_exception_filter import setup_exception_handlers
from app.core.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("アプリケーションを起動します")
    if os.getenv("DATABASE_SYNC", "false").lower() == "true":
        import app.adapter.infrastructure.db  # noqa: F401

        Base.metadata.create_all(bind=engine)
        logger.info("データベーススキーマを同期しました")
    yield
    logger.info("アプリケーションを終了します")


app = FastAPI(lifespan=lifespan)

setup_exception_handlers(app)
app.include_router(artist_router, prefix="/artists", tags=["artists"])
