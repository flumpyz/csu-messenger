from pydantic import BaseModel

from datetime import datetime
from enums.chatType import ChatType


class Chat(BaseModel):
    name: str
    type: ChatType


class ChatCreate(Chat):
    created_date: datetime


class ChatInDB(Chat):
    id: int

    class Config:
        orm_mode = True
