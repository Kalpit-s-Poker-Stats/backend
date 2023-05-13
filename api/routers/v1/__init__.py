from fastapi import APIRouter
from api.routers.v1 import (
    account,
)

router = APIRouter(prefix="/v1")

router.include_router(router=account.router)