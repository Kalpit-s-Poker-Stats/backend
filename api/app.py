import api.middleware
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
import logging
from api.config import app
from api.routers import (
    v1,
)

logger = logging.getLogger(__name__)

app.include_router(v1.router)


@app.get("/")
async def root():
    return {
        "message": "BFF for a Poker Winnings Tracker"
    }
