from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PlayerData(BaseModel):
    player_nickname: str
    player_id: str
    session_start_at: Optional[datetime] = None
    session_end_at: Optional[datetime] = None
    buy_in: Optional[float] = None
    stack: float
    net: float