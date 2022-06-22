from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from deps import get_db, get_current_user
import crud.chat as crud
from schemas.chat import Chat, ChatInDB, ChatCreate
from schemas.user import User, UserInDB
from schemas.userChat import UserChatInDB
from schemas.chatUsers import UserInChat, ChatUsers

router = APIRouter(prefix="/chat")


@router.get("/", response_model=ChatUsers)
async def get_chat(chat_id: int, user_id=Depends(get_current_user), db=Depends(get_db)):
    """Получить чат по заданному chat_id"""
    chat_db = crud.get_chat_by_id(db=db, chat_id=chat_id)
    users = crud.get_users_by_chat_id(db=db, chat_id=chat_id)

    if chat_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    chat_users = ChatUsers(id=chat_db.id,
                           name=chat_db.name,
                           type=chat_db.type,
                           created_date=chat_db.created_date,
                           users=users)

    return chat_users


@router.post("/", response_model=ChatInDB)
async def create_chat(chat: ChatCreate, users_id: List[int], user_id=Depends(get_current_user), db=Depends(get_db)):
    """Создать чат"""
    result = crud.create_chat(db=db, chat=chat)
    crud.add_users_to_chat(db=db, chat_id=result.id, users_id=users_id)
    return result


@router.put("/{chat_id}", response_model=ChatInDB)
async def update_chat(chat: Chat, chat_id: int, user_id=Depends(get_current_user), db=Depends(get_db)):
    """Изменить чат"""
    chat_db = crud.update_chat(db=db, chat_id=chat_id, chat=chat)
    return chat_db


@router.put("/", response_model=ChatInDB)
async def add_user_to_chat(chat_id: int, user_to_chat_id: int, user_id=Depends(get_current_user), db=Depends(get_db)):
    """Добавить юзера в чат"""
    result = crud.add_user_to_chat(db=db, chat_id=chat_id, user_id=user_to_chat_id)
    return result


@router.delete("/{chat_id}")
async def delete_chat(chat_id: int, user_id=Depends(get_current_user), db=Depends(get_db)):
    """Удалить чат"""
    crud.delete_chat(db=db, chat_id=chat_id)
