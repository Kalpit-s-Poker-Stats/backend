from pydantic import BaseModel
from typing import Union
from datetime import datetime

class Ledger(BaseModel):
    player_nickname: str
    player_idL: str
    session_start_at: datetime
    session_end_at: datetime
    buy_in: float