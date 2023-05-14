from fastapi import APIRouter
from api.routers.v1 import (
    profile,
    session
)

router = APIRouter(prefix="/v1")

router.include_router(router=profile.router)
router.include_router(router=session.router)