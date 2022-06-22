from pydantic import BaseModel

from datetime import datetime


class Message(BaseModel):
    chat_id: int
    user_id: int
    message_text: str


class MessageCreate(Message):
    sending_datetime: datetime


class MessageInDB(Message):
    id: int

    class Config:
        orm_mode = True
