from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    pn_id: str
    splitwise_email: str
    discord_username: str
    acknowledgment: bool