import json

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select, insert, delete, update
from sqlalchemy.exc import IntegrityError

from api.database.database import USERDATA_ENGINE
from api.database.functions import sqlalchemy_result

from api.database.models import (
    Profile
)

from api.models.UserCreate import UserCreate

from datetime import date
import http.client
from api import config
import http.server
from urllib.parse import urlparse, parse_qs

router = APIRouter()

@router.get("/get_user_data")
async def full_table(id) -> json:
    data = await get_user_info(id)

    response = dict()
    response[0] = data
   
    return response


async def get_user_info(id):
    sql = select(Profile).where(Profile.pn_id == id)
    async with USERDATA_ENGINE.get_session() as session:
            session: AsyncSession = session
            async with session.begin():
                data = await session.execute(sql)

    data = sqlalchemy_result(data)
    data = data.rows2dict()
    if len(data) == 0:
        raise HTTPException(detail = "Profile not found")
    return data

# TODO: update query to add in values for the updated columns in profile table
@router.put("/reset_user_stats")
async def reset_user_stats(id):
    default_date = "0000-00-00"
    sql = update(Profile).values(all_time_total = 0, biggest_win = 0, biggest_loss = 0, date_of_biggest_win = date(1000, 1, 1), date_of_biggest_loss = date(1000, 1, 1), average_all_time_win_or_loss = 0, positive_percentage = 0, negative_percentage = 0, number_of_sessions_positive = 0, number_of_sessions_negative = 0, total_sessions_played = 0).where(Profile.pn_id == id)
    async with USERDATA_ENGINE.get_session() as session:
            session: AsyncSession = session
            async with session.begin():
                data = await session.execute(sql)

    return 'User with id = ' + id + " has been reset."


@router.post("/create_user_profile")
async def create_user_profile(userModel: UserCreate):
    splitwise_id = 1234567890
    splitwise_id = await get_splitwise_id_from_splitwise(userModel.splitwise_email)
    print(splitwise_id)
    if(splitwise_id == None):
        raise HTTPException(status_code=404, detail="User Could Not be Created because email is not assocaited with any splitwise account")
    sql = insert(Profile).values(name = userModel.name, pn_id = userModel.pn_id, splitwise_id = splitwise_id, discord_username = userModel.discord_username, all_time_total = 0, biggest_win = 0, biggest_loss = 0, date_of_biggest_win = date(1000, 1, 1), date_of_biggest_loss = date(1000, 1, 1), average_all_time_win_or_loss = 0, positive_percentage = 0, negative_percentage = 0, number_of_sessions_positive = 0, number_of_sessions_negative = 0, total_sessions_played = 0, acknowledgment_accepted = userModel.acknowledgment)
    try:
        async with USERDATA_ENGINE.get_session() as session:
                session: AsyncSession = session
                async with session.begin():
                    data = await session.execute(sql)

        return 'User with id = ' + userModel.pn_id + " has been created."
    except IntegrityError as e:
        if "Duplicate entry" in str(e.orig):
            raise HTTPException(status_code=409, detail="User not created because pn_id: " + userModel.pn_id + " exists in the DB already")
        else:
            raise HTTPException(status_code=400, detail="Generic Error from DB")
    except HTTPException as e:
        raise e 
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error", "error": str(e)})



async def get_splitwise_id_from_splitwise(splitwise_email):
    conn = http.client.HTTPSConnection(config.splitwise_url)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + config.splitwise_api_key,
    }
    print(headers)
    
    try:
        conn.request("GET", "/api/v3.0/get_group/63939034", headers=headers)
        response = conn.getresponse()

        # print(response.read().decode())
        if(response.status != 200):
            print("inside status not 200")
            logger.error(json.dumps({"error": f"Request failed with status {response.status}"}).encode())
            return

        data = response.read()
        data = json.loads(data.decode('utf-8'))
        print(data)
        print("right after data")
        return find_splitwise_id_from_members(data['group']['members'], splitwise_email)
    except Exception as e:
        return json.dumps({"error": str(e)}).encode(), 500
    finally:
        conn.close()


def find_splitwise_id_from_members(data, email):
    for item in data:
        if item['email'] == email:
            return item['id']
    return None
