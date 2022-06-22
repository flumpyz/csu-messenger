from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import Boolean

from core.db.models import Message
from core.db.models import Chat
from core.db.models import UserChat
from core.db.models import UserMessage
from enums.messageStatusType import MessageStatusType
import schemas.message as schema
import schemas.userMessage as schemaUserMessage


def create_message(db: Session, message: schema.MessageCreate):
    message_db = Message(chat_id=message.chat_id,
                         user_id=message.user_id,
                         message_text=message.message_text,
                         sending_datetime=message.sending_datetime)
    db.add(message_db)

    users_db = db.query(UserChat).filter(UserChat.chat_id == message.chat_id).all()

    for user_db in users_db:
        db.add(UserMessage(user_id=user_db.user_id,
                           message_id=message_db.id,
                           status=MessageStatusType.sent,
                           is_changed=False))

    db.commit()

    return message_db


def get_message_by_id(db: Session, message_id: int):
    return db.query(Message).filter(Message.id == message_id).one_or_none()


def update_message(db: Session, message_id: int, message: schema.Message):
    message_db = db.query(Message).filter(Message.id == message_id).one_or_none()
    users_messages_db = db.query(UserMessage).filter(UserMessage.message_id == message_id).all()

    for param, value in message.dict().items():
        setattr(message_db, param, value)

    for user_message_db in users_messages_db:
        user_message_db.is_changed = True

    db.commit()

    return message_db


def delete_message(db: Session, message_id: int):
    db.query(UserMessage).filter(UserMessage.message_id == message_id).delete()
    db.query(Message).filter(Message.id == message_id).delete()
    db.commit()


def get_n_last_messages_by_chat_id(db: Session, chat_id: int, count: int, user_id: int):
    now = datetime.now()
    messages_db = db.query(Message).where(Message.sending_datetime < now).filter(Message.chat_id == chat_id).order_by(Message.sending_datetime.desc())[:count]
    messages_id = []

    for message_db in messages_db:
        messages_id.append(message_db.id)
        author_user_message = db.query(UserMessage) \
            .filter(UserMessage.user_id == message_db.user_id) \
            .filter(UserMessage.message_id == message_db.id) \
            .one_or_none()
        if message_db.user_id != user_id and author_user_message.status != MessageStatusType.read:
            author_user_message.status = MessageStatusType.read
    db.commit()

    user_messages_db = db.query(UserMessage) \
        .where(UserMessage.message_id.in_(messages_id)) \
        .filter(UserMessage.user_id == user_id).all()

    for user_message_db in user_messages_db:
        user_message_db.status = MessageStatusType.read
    db.commit()

    db.commit()

    return messages_db
