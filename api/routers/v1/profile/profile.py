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

from datetime import date

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

@router.put("/reset_user_stats")
async def reset_user_stats(id):
    default_date = "0000-00-00"
    sql = update(Profile).values(all_time_total = 0, biggest_win = 0, biggest_loss = 0, date_of_biggest_win = date(1000, 1, 1), date_of_biggest_loss = date(1000, 1, 1), average_all_time_win_or_loss = 0, positive_percentage = 0, negative_percentage = 0, number_of_sessions_positive = 0, number_of_sessions_negative = 0, total_sessions_played = 0).where(Profile.id == id)
    async with USERDATA_ENGINE.get_session() as session:
            session: AsyncSession = session
            async with session.begin():
                data = await session.execute(sql)

    return 'User with id = ' + id + " has been reset."