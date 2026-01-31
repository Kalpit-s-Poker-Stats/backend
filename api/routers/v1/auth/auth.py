import os
import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.database.database import USERDATA_ENGINE
from api.database.models import Profile

router = APIRouter()

# Discord OAuth Configuration
DISCORD_CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.environ.get("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = os.environ.get("DISCORD_REDIRECT_URI")
DISCORD_API_URL = "https://discord.com/api/v10"


class DiscordAuthRequest(BaseModel):
    code: str


@router.post("/discord")
async def discord_auth(request: DiscordAuthRequest):
    """
    Handle Discord OAuth callback.
    1. Exchange authorization code for access token
    2. Fetch user info from Discord
    3. Match user by discord_username in database
    4. Return user data
    """
    try:
        # Exchange code for access token
        token_data = await exchange_code_for_token(request.code)
        access_token = token_data.get("access_token")

        if not access_token:
            raise HTTPException(status_code=400, detail="Failed to get access token from Discord")

        # Fetch user info from Discord
        discord_user = await fetch_discord_user(access_token)

        discord_id = discord_user.get("id")
        discord_username = discord_user.get("username")
        global_name = discord_user.get("global_name")  # Display name
        avatar = discord_user.get("avatar")

        # Build avatar URL if available
        picture = None
        if avatar:
            picture = f"https://cdn.discordapp.com/avatars/{discord_id}/{avatar}.png"

        # Try to find existing user by discord_username
        user = await find_user_by_discord_username(discord_username)

        if user:
            # Update user's discord_id if not already set
            if not user.discord_id:
                await update_user_discord_id(user.pn_id, discord_id)

            return JSONResponse(
                status_code=200,
                content={
                    "user": {
                        "pn_id": user.pn_id,
                        "name": user.name or global_name or discord_username,
                        "discord_id": discord_id,
                        "discord_username": discord_username,
                        "picture": picture
                    }
                }
            )
        else:
            # User not found - return Discord info without creating account
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "user_not_found",
                    "message": f"No account found for Discord user '{discord_username}'. Please contact an admin to link your account.",
                    "discord_username": discord_username
                }
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Discord authentication failed: {str(e)}")


async def exchange_code_for_token(code: str) -> dict:
    """Exchange authorization code for access token."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DISCORD_API_URL}/oauth2/token",
            data={
                "client_id": DISCORD_CLIENT_ID,
                "client_secret": DISCORD_CLIENT_SECRET,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": DISCORD_REDIRECT_URI
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=f"Discord token exchange failed: {response.text}"
            )

        return response.json()


async def fetch_discord_user(access_token: str) -> dict:
    """Fetch user info from Discord API."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DISCORD_API_URL}/users/@me",
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to fetch Discord user: {response.text}"
            )

        return response.json()


async def find_user_by_discord_username(discord_username: str):
    """Find user in database by discord_username."""
    sql = select(Profile).where(Profile.discord_username == discord_username)
    async with USERDATA_ENGINE.get_session() as session:
        session: AsyncSession = session
        async with session.begin():
            result = await session.execute(sql)
            return result.scalars().first()


async def update_user_discord_id(pn_id: str, discord_id: str) -> None:
    """Update user's discord_id in database."""
    sql = update(Profile).where(Profile.pn_id == pn_id).values(discord_id=discord_id)
    async with USERDATA_ENGINE.get_session() as session:
        session: AsyncSession = session
        async with session.begin():
            await session.execute(sql)
