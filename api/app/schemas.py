from datetime import datetime

from pydantic import BaseModel


class PostOut(BaseModel):
    id: int
    url: str
    title: str
    description: str
    date_published: datetime


class PostList(BaseModel):
    data: list[PostOut]
