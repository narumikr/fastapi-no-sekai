import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.adapter.controllers.artist_controller import router as artist_router
from app.core.database import Base, engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    if os.getenv("DATABASE_SYNC") == "true":
        import app.adapter.infrastructure.db  # noqa: F401

        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(artist_router, prefix="/artists", tags=["artists"])
