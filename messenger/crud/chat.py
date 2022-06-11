from sqlalchemy.orm import Session

from datetime import datetime
from enums.chatType import ChatType
from core.db.models import Chat
from core.db.models import UserChat
import schemas.chat as schemaChat
import schemas.userChat as schemaUserChat

chat_database = [
    {
        "id": 1,
        "name": "Чат 1",
        "created_date": datetime(2022, 4, 20, 19, 39, 0),
        "type": ChatType.group,
    }
]

user_chat_database = [
    {
        "user_id": 1,
        "chat_id": 1
    },
    {
        "user_id": 2,
        "chat_id": 1
    },
]


def create_chat(db: Session, chat: schemaChat.ChatCreate):
    chat_db = Chat(name=chat.name, created_date=chat.created_date, type=chat.type)
    db.add(chat_db)
    db.commit()

    return chat_db


def get_chat_by_id(db: Session, chat_id: int):
    return db.query(Chat).filter(Chat.id == chat_id).one_or_none()


def update_chat(db: Session, chat_id: int, chat: schemaChat.Chat):
    chat_db = db.query(Chat).filter(Chat.id == chat_id).one_or_none()
    for param, value in chat.dict().items():
        setattr(chat_db, param, value)
    db.commit()

    return chat_db


def delete_chat(db: Session, chat_id: int):
    chat_db = db.query(Chat).filter(Chat.id == chat_id).delete()
    db.commit()


def add_user_to_chat(db: Session, user_id: int, chat_id: int):
    user_chat_db = UserChat(user_id=user_id, chat_id=chat_id)
    db.add(user_chat_db)
    db.commit()

    return get_chat_by_id(db, chat_id=chat_id)


def get_users_by_chat_id(db: Session, chat_id: int):
    return db.query(UserChat).filter(Chat.id == chat_id).all()
