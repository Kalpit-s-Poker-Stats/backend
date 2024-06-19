import json
from datetime import date

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select, insert, delete, update
from pydantic import BaseModel

from api.database.database import USERDATA_ENGINE
from api.database.functions import sqlalchemy_result

from pydantic import BaseModel

from api.models.PlayerData import PlayerData

from api.database.models import (
    Session,
    Profile
)

from api.routers.v1.profile import profile
import datetime
from datetime import datetime
from typing import Union
import pandas as pd

import http.client
from api import config
import http.server
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from typing import List, Optional


import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    sql2 = select(Profile).where(Profile.pn_id == id)
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


@router.get("/bulk_upload_tester")
async def bulk_upload_tester() -> json: 
    df = pd.read_excel('tester.xlsx')

    # Initialize variables
    table_data = []
    header_row = None
    table_started = False

    # Iterate over rows
    for index, row in df.iterrows():
        # Check if the row starts a new table
        if row.notnull().all() and not table_started:
            table_started = True
            header_row = row
        # Check if the row is empty, indicating the end of a table
        elif not row.notnull().any() and table_started:
            table_started = False
            # Process table data
            data = []
            for i in range(1, len(header_row), 2):
                user = header_row[i]
                print("user: " + user)
                date = row[i]
                print("date: " + date)
                amount = row[i+1]
                print("amount: " + amount)
                data.append({'user': user, 'date': date, 'amount': amount})
            table_data.extend(data)


@router.post("/submit_ledger", response_model=List[PlayerData])
async def submit_ledger(ledger: List[PlayerData]) -> json:
    # print(ledger)
    # validate_pn_ids(ledger)
    for item in ledger:
        print(item)
        await update_user_stats(item.player_id, item.net, datetime.now().date())
        if(item.player_id == '5CsKvXEd3O'):
            continue
        await create_splitwise_expenses(item.player_id, item.net)


# async def validate_pn_ids(ledger: List[PlayerData]):



#
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
    
    sql = update(Profile).values(all_time_total = all_time_total, biggest_win = biggest_win, biggest_loss = biggest_loss, date_of_biggest_win = date_of_biggest_win, date_of_biggest_loss = date_of_biggest_loss, average_all_time_win_or_loss = average_all_time_win_or_loss, positive_percentage = positive_percentage, negative_percentage = negative_percentage, number_of_sessions_positive = number_of_sessions_positive, number_of_sessions_negative = number_of_sessions_negative, total_sessions_played = total_sessions_played).where(Profile.pn_id == id)
    async with USERDATA_ENGINE.get_session() as session:
            session: AsyncSession = session
            async with session.begin():
                await session.execute(sql)             
    return True


async def create_splitwise_expenses(id, winnings):
    print("id in create splitwise expenses")
    print(id)
    sw_id = await get_splitwise_id(id, winnings)
    logger.info("sw_id: " + str(sw_id))
    expense_data = {}
    if(winnings > 0):
        expense_data = {
            "cost": str(winnings),
            "description": 'Poke Winner',
            "group_id": "63939034",
            "split_equally": "false",
            "users__0__user_id": "44365391",
            "users__0__paid_share": 0,
            "users__0__owed_share": str(winnings),
            "users__1__user_id": sw_id,
            "users__1__paid_share": str(winnings),
            "users__1__owed_share": 0,
        }
    elif(winnings < 0):
        expense_data = {
            "cost": str(-1*winnings),
            "description": 'Poke Loser',
            "group_id": "63939034",
            "split_equally": "false",
            "users__0__user_id": "44365391",
            "users__0__paid_share": str(-1*winnings),
            "users__0__owed_share": 0,
            "users__1__user_id": sw_id,
            "users__1__paid_share": 0,
            "users__1__owed_share": str(-1*winnings),
        }

    print(expense_data)

    conn = http.client.HTTPSConnection(config.splitwise_url)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + config.splitwise_api_key,
    }
    print(headers)
    
    try:
        conn.request("POST", "/api/v3.0/create_expense", body=json.dumps(expense_data), headers=headers)
        response = conn.getresponse()
        print("made it here")
        print(response.read().decode())
        if(response.status != 200):
            print("inside status not 200")
            logger.error(json.dumps({"error": f"Request failed with status {response.status}"}).encode())
            return

        data = response.read()
        data = json.loads(data.decode('utf-8'))
        print(data)
        print("right after data")
    except Exception as e:
        return json.dumps({"error": str(e)}).encode(), 500
    finally:
        conn.close()

    print(json.dumps(data).encode())
    print("right after data.encode")


async def get_splitwise_id(pn_id, winnings):
    sql = select(Profile).where(Profile.pn_id == pn_id)
    async with USERDATA_ENGINE.get_session() as session:
            session: AsyncSession = session
            async with session.begin():
                result = await session.execute(sql)
                data = result.scalars().first()

            if(data):
                return data.splitwise_id