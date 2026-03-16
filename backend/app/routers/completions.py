import json

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.dependencies import get_current_user
from app.models.chats import Chat, Message
from app.models.users import User
from app.schemas.chats import ChatCompletionRequest
from app.utils.streaming import stream_chat_completion

router = APIRouter(prefix="/api/chat", tags=["completions"])


@router.post("/completions")
async def chat_completions(
    body: ChatCompletionRequest,
    chat_id: str | None = None,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Validate chat ownership if chat_id provided
    chat = None
    if chat_id:
        result = await db.execute(
            select(Chat).where(Chat.id == chat_id, Chat.user_id == user.id)
        )
        chat = result.scalar_one_or_none()
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
            )

    request_body = {
        "model": body.model,
        "messages": [{"role": m.role, "content": m.content} for m in body.messages],
    }

    if body.stream:
        collected_content: list[str] = []

        async def generate():
            async for chunk in stream_chat_completion(request_body):
                # Collect content for DB storage
                if chunk.startswith("data: ") and chunk.strip() != "data: [DONE]":
                    try:
                        data = json.loads(chunk[6:].strip())
                        delta_content = (
                            data.get("choices", [{}])[0]
                            .get("delta", {})
                            .get("content", "")
                        )
                        if delta_content:
                            collected_content.append(delta_content)
                    except (json.JSONDecodeError, IndexError):
                        pass
                yield chunk

            # Save messages to DB after streaming completes
            if chat:
                user_msg = body.messages[-1]
                db.add(Message(
                    chat_id=chat.id,
                    role=user_msg.role,
                    content=user_msg.content,
                ))
                db.add(Message(
                    chat_id=chat.id,
                    role="assistant",
                    content="".join(collected_content),
                    model=body.model,
                ))
                # Update chat title from first user message if still default
                if chat.title == "New Chat" and body.messages:
                    first_content = body.messages[0].content
                    chat.title = first_content[:50] + ("..." if len(first_content) > 50 else "")
                await db.commit()

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    # Non-streaming mode
    import aiohttp
    from app.config import settings

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{settings.OPENAI_API_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={**request_body, "stream": False},
        ) as response:
            result = await response.json()

    if chat:
        user_msg = body.messages[-1]
        assistant_content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        db.add(Message(chat_id=chat.id, role=user_msg.role, content=user_msg.content))
        db.add(Message(
            chat_id=chat.id, role="assistant", content=assistant_content, model=body.model,
        ))
        if chat.title == "New Chat" and body.messages:
            first_content = body.messages[0].content
            chat.title = first_content[:50] + ("..." if len(first_content) > 50 else "")
        await db.commit()

    return result
