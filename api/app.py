import api.middleware
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
        "message": "Welcome to the Workout with Me API. If you're interested in becoming a developer, please contact ferrariictweet@gmail.com!"
    }
