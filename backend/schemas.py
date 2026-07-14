from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    nickname: str = "익명"
    password: str


class PostUpdate(PostBase):
    password: str


class PostDelete(BaseModel):
    password: str


class PostListItem(BaseModel):
    id: int
    place_id: int
    nickname: str
    title: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostDetail(PostBase):
    id: int
    place_id: int
    nickname: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaginatedPosts(BaseModel):
    items: List[PostListItem]
    total: int
    page: int
    size: int


class ChatSummaryRequest(BaseModel):
    place_id: Optional[int] = None
    question: Optional[str] = None


class ChatSummaryResponse(BaseModel):
    summary: str
