import json
from datetime import date

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select, insert, delete, update
from pydantic import BaseModel

from api.database.database import USERDATA_ENGINE
from api.database.functions import sqlalchemy_result

from api.database.models import (
    Session,
    Profile
)

from api.routers.v1.profile import profile
import datetime
from datetime import datetime
from typing import Union


router = APIRouter()

class SessionEntry(BaseModel):
    id: int
    winnings: float
    buy_in_amount: float
    buy_out_amount: float
    location: str
    date: str


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
async def entry(session_entry: SessionEntry):
    sql = insert(Session).values(id = session_entry.id, winnings = session_entry.winnings, buy_in_amount = session_entry.buy_in_amount, buy_out_amount = session_entry.buy_out_amount, location = session_entry.location, date = session_entry.date)
    current_profile = await update_user_stats(session_entry.id, session_entry.winnings, session_entry.date)


    async with USERDATA_ENGINE.get_session() as session:
            session: AsyncSession = session
            async with session.begin():
                await session.execute(sql)
    raise HTTPException(status_code = status.HTTP_201_CREATED, detail = "Session Added for id = " + str(session_entry.id))

@router.get("/user_data")
async def user_data(id, beg_date: Union[str, None] = None, end_date: Union[str, None] = None) -> json:
    current_date = date.today()
    sql = select(Session).where(Session.id == id)
    sql2 = select(Profile).where(Profile.id == id)
    if(beg_date):
        sql = sql.filter(Session.date >= beg_date)
    if(end_date):
        sql = sql.filter(Session.date <= end_date)
    async with USERDATA_ENGINE.get_session() as session:
            session: AsyncSession = session
            async with session.begin():
                data = await session.execute(sql)
                data2 = await session.execute(sql2)
    data = sqlalchemy_result(data)
    data = data.rows2dict()
    data2 = sqlalchemy_result(data2)
    data2 = data2.rows2dict()
    data += data2


    return data



async def update_user_stats(id, winnings, date):
    winnings = float(winnings)
    current_profile = await profile.get_user_info(id)
    total_sessions_played = current_profile[0].get('total_sessions_played') + 1
    all_time_total = float(current_profile[0].get('all_time_total')) + winnings
    average_all_time_win_or_loss = all_time_total / total_sessions_played
    if (current_profile[0].get('biggest_win') < winnings):
        biggest_win = winnings
        date_of_biggest_win = date
        biggest_loss = current_profile[0].get('biggest_loss')
        date_of_biggest_loss = current_profile[0].get('date_of_biggest_loss')
    elif(current_profile[0].get('biggest_loss') > winnings):
        biggest_loss = winnings
        date_of_biggest_loss = date
        biggest_win = current_profile[0].get('biggest_win')
        date_of_biggest_win = current_profile[0].get('date_of_biggest_win')
    else:
        biggest_loss = current_profile[0].get('biggest_loss')
        date_of_biggest_loss = current_profile[0].get('date_of_biggest_loss')
        biggest_win = current_profile[0].get('biggest_win')
        date_of_biggest_win = current_profile[0].get('date_of_biggest_win')
    if(winnings >= 0):
        number_of_sessions_positive = current_profile[0].get('number_of_sessions_positive') + 1
        positive_percentage = (number_of_sessions_positive / total_sessions_played) * 100
        negative_percentage = (current_profile[0].get('number_of_sessions_negative') / total_sessions_played) * 100
        number_of_sessions_negative = current_profile[0].get('number_of_sessions_negative')
    if(winnings < 0):
        number_of_sessions_negative = current_profile[0].get('number_of_sessions_negative') + 1
        negative_percentage = (number_of_sessions_negative / total_sessions_played) * 100
        positive_percentage = (current_profile[0].get('number_of_sessions_positive') / total_sessions_played) * 100
        number_of_sessions_positive = current_profile[0].get('number_of_sessions_positive')
    
    sql = update(Profile).values(all_time_total = all_time_total, biggest_win = biggest_win, biggest_loss = biggest_loss, date_of_biggest_win = date_of_biggest_win, date_of_biggest_loss = date_of_biggest_loss, average_all_time_win_or_loss = average_all_time_win_or_loss, positive_percentage = positive_percentage, negative_percentage = negative_percentage, number_of_sessions_positive = number_of_sessions_positive, number_of_sessions_negative = number_of_sessions_negative, total_sessions_played = total_sessions_played).where(Profile.id == id)
    async with USERDATA_ENGINE.get_session() as session:
            session: AsyncSession = session
            async with session.begin():
                await session.execute(sql)             
    return True