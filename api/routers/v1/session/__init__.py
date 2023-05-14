from fastapi import APIRouter

from api.routers.v1.session import session

router = APIRouter(prefix="/session")
router.include_router(router=session.router)
