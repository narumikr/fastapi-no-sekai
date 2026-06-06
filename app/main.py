from fastapi import FastAPI

from app.adapter.controllers.artist_controller import router as artist_router

app = FastAPI()

app.include_router(artist_router, prefix="/artists", tags=["artists"])
