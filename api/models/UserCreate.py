from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    pn_id: str
    splitwise_email: str
    discord_username: str
    discord_id: Optional[str] = None
    acknowledgment: bool