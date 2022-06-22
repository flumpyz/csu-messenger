from pydantic import BaseModel

from enums.messageStatusType import MessageStatusType


class UserMessage(BaseModel):
    user_id: int
    message_id: int
    status: MessageStatusType
    is_changed: bool


class UserMessageInDB(UserMessage):
    id: int

    class Config:
        orm_mode = True
