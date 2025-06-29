from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class PostOut(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, validate_by_alias=False, serialize_by_alias=True
    )

    id: int
    url: str
    title: str
    description: str
    date_published: datetime


class PostList(BaseModel):
    data: list[PostOut]


class ItemList(BaseModel):
    data: list[str]


class FilterPost(BaseModel):
    p: int = Field(1, gt=0)
    pp: int = Field(50, gt=0, le=50)
    sort_by: str = "date_published"
    order: Literal["desc", "asc"] = "desc"
    q: str | None = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class SourceCount(BaseModel):
    source: str
    count: int


class SubjectCount(BaseModel):
    subject: str
    count: int


class Stats(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, validate_by_alias=False, serialize_by_alias=True
    )

    total_news: int
    today: int
    news_by_subjects: list[SubjectCount]
    news_by_sources: list[SourceCount]
