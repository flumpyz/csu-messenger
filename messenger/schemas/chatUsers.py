from datetime import datetime
from typing import List

from pydantic import BaseModel

from enums.chatType import ChatType


class UserInChat(BaseModel):
    id: int
    login: str
    name: str


class ChatUsers(BaseModel):
    id: int
    name: str
    type: ChatType
    created_date: datetime
    users: List[UserInChat]
