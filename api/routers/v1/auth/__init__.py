from fastapi import APIRouter

from api.routers.v1.auth import auth

router = APIRouter(prefix="/auth")
router.include_router(router=auth.router)
