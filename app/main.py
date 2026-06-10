import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import engine

from app.adapter.controllers.artist_controller import router as artist_router
from app.adapter.infrastructure.db.base_entity import Base
from app.core.database import engine

@asynccontextmanager
async def lifespan(_: FastAPI):
    if os.getenv("DATABASE_SYNC") == "true":
        import app.adapter.infrastructure.db  # noqa: F401

        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(artist_router, prefix="/artists", tags=["artists"])
