import api.middleware
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
import logging
from api.config import app
from api.routers import (
    v1,
)

logger = logging.getLogger(__name__)

origins = [
    "http://135.148.121.103:4200",
    "http://localhost:4200" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can restrict allowed methods if needed
    allow_headers=["*"],  # You can restrict allowed headers if needed
)



app.include_router(v1.router)


@app.get("/")
async def root():
    return {
        "message": "BFF for a Poker Winnings Tracker"
    }
