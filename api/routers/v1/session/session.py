import json

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select, insert, delete, update

from api.database.database import USERDATA_ENGINE
from api.database.functions import sqlalchemy_result

from api.database.models import (
    Session
)

router = APIRouter()


@router.get("/full_session_table")
async def full_session_table() -> json:
    sql = select(Session).where()
    async with USERDATA_ENGINE.get_session() as session:
            session: AsyncSession = session
            async with session.begin():
                data = await session.execute(sql)

    data = sqlalchemy_result(data)
    data = data.rows2dict()
    response = dict()
    for value in data:
        idx = value['id']
        response[idx] = value
   
    return response


@router.post("/entry")
async def entry(id, winnings, buy_in_amount, buy_out_amount, location):
    sql = insert(Session).values(id = id, winnings = winnings, buy_in_amount = buy_in_amount, buy_out_amount = buy_out_amount, location = location)
    async with USERDATA_ENGINE.get_session() as session:
            session: AsyncSession = session
            async with session.begin():
                await session.execute(sql)
    raise HTTPException(status_code = status.HTTP_201_CREATED, detail = "Account Added")


