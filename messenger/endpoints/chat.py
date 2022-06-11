from fastapi import APIRouter, Depends, HTTPException, status

from deps import get_db
import crud.chat as crud
from schemas.chat import Chat, ChatInDB, ChatCreate

router = APIRouter(prefix="/chat")


@router.get("/", response_model=ChatInDB)
async def get_chat(chat_id: int, db=Depends(get_db)):
    """Получить чат по заданному chat_id"""
    chat = crud.get_chat_by_id(db=db, chat_id=chat_id)
    users = crud.get_users_by_chat_id(db=db, chat_id=chat_id)
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return chat, users


@router.post("/", response_model=ChatInDB)
async def create_chat(chat: ChatCreate, db=Depends(get_db)):
    """Создать чат"""
    result = crud.create_chat(db=db, chat=chat)
    return result


@router.put("/{chat_id}", response_model=ChatInDB)
async def update_chat(chat: Chat, chat_id: int, db=Depends(get_db)):
    """Изменить чат"""
    chat_db = crud.update_chat(db=db, chat_id=chat_id, chat=chat)
    return chat_db


@router.delete("/{chat_id}")
async def delete_chat(chat_id: int, db=Depends(get_db)):
    """Удалить чат"""
    crud.delete_chat(db=db, chat_id=chat_id)
