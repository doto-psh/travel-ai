from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.dependencies import get_current_user
from app.models.chats import Chat, Message
from app.models.users import User
from app.schemas.chats import (
    ChatCreateRequest,
    ChatUpdateRequest,
    ChatResponse,
    ChatDetailResponse,
)

router = APIRouter(prefix="/api/chats", tags=["chats"])


@router.get("/", response_model=list[ChatResponse])
async def list_chats(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Chat)
        .where(Chat.user_id == user.id)
        .order_by(Chat.updated_at.desc())
    )
    return result.scalars().all()


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def create_chat(
    body: ChatCreateRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    chat = Chat(user_id=user.id, title=body.title)
    db.add(chat)
    await db.commit()
    await db.refresh(chat)
    return chat


@router.get("/{chat_id}", response_model=ChatDetailResponse)
async def get_chat(
    chat_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Chat)
        .options(selectinload(Chat.messages))
        .where(Chat.id == chat_id, Chat.user_id == user.id)
    )
    chat = result.scalar_one_or_none()
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    return chat


@router.put("/{chat_id}", response_model=ChatResponse)
async def update_chat(
    chat_id: str,
    body: ChatUpdateRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Chat).where(Chat.id == chat_id, Chat.user_id == user.id)
    )
    chat = result.scalar_one_or_none()
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")

    chat.title = body.title
    await db.commit()
    await db.refresh(chat)
    return chat


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(
    chat_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Chat).where(Chat.id == chat_id, Chat.user_id == user.id)
    )
    chat = result.scalar_one_or_none()
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")

    await db.delete(chat)
    await db.commit()
