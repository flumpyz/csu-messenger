from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from deps import get_db, get_current_user
import crud.message as crud
from schemas.message import Message, MessageInDB, MessageCreate

router = APIRouter(prefix="/message")


@router.get("/", response_model=MessageInDB)
async def get_message(message_id: int,
                      user_id=Depends(get_current_user),
                      db=Depends(get_db)):
    """Получить сообщение по заданному message_id"""
    message = crud.get_message_by_id(db=db, message_id=message_id)

    if message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return message


@router.post("/", response_model=MessageInDB)
async def create_message(message: MessageCreate,
                         user_id=Depends(get_current_user),
                         db=Depends(get_db)):
    """Создать сообщение"""
    result = crud.create_message(db=db, message=message)
    return result


@router.put("/{message_id}", response_model=MessageInDB)
async def update_message(message: Message,
                         message_id: int,
                         user_id=Depends(get_current_user),
                         db=Depends(get_db)):
    """Изменить сообщение"""
    message_db = crud.update_message(db=db, message_id=message_id, message=message)
    return message_db


@router.delete("/{message_id}")
async def delete_message(message_id: int,
                         user_id=Depends(get_current_user),
                         db=Depends(get_db)):
    """Удалить сообщение"""
    crud.delete_message(db=db, message_id=message_id)


@router.get("/last", response_model=List[MessageInDB])
async def get_n_last_messages_by_chat_id(chat_id: int,
                                         message_count: int,
                                         db=Depends(get_db),
                                         user_id=Depends(get_current_user)):
    """Получить список из последних n сообщений по chat_id"""
    messages_db = crud.get_n_last_messages_by_chat_id(db=db, chat_id=chat_id, count=message_count, user_id=user_id)
    return messages_db
