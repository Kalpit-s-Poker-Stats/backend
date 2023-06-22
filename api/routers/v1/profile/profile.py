import json

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select, insert, delete, update

from api.database.database import USERDATA_ENGINE
from api.database.functions import sqlalchemy_result

from api.database.models import (
    Profile
)

router = APIRouter()

@router.get("/get_user_data")
async def full_table(id) -> json:
    data = await get_user_info(id)

    response = dict()
    response[0] = data
   
    return response


async def get_user_info(id):
    sql = select(Profile).where(Profile.id == id)
    async with USERDATA_ENGINE.get_session() as session:
            session: AsyncSession = session
            async with session.begin():
                data = await session.execute(sql)

    data = sqlalchemy_result(data)
    data = data.rows2dict()
    if len(data) == 0:
        raise HTTPException(detail = "Profile not found")
    return data