from datetime import datetime

from pydantic import BaseModel


class MessageBase(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = "gpt-4o"
    messages: list[MessageBase]
    stream: bool = True


class MessageResponse(BaseModel):
    id: str
    chat_id: str
    role: str
    content: str
    model: str | None = None
    token_count: int | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ChatDetailResponse(ChatResponse):
    messages: list[MessageResponse] = []


class ChatCreateRequest(BaseModel):
    title: str = "New Chat"


class ChatUpdateRequest(BaseModel):
    title: str
