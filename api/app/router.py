from datetime import date, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.schemas import FilterPost, ItemList, PostList, SourceCount, Stats, SubjectCount
from core.database import get_session
from core.models import Post

router = APIRouter(prefix="/api/v1", tags=["api_v1"])

DBSession = Annotated[Session, Depends(get_session)]


@router.get("/posts", response_model=PostList)
def read_posts(session: DBSession, filter: Annotated[FilterPost, Query()]):
    # Filtra em titulo e descrição dos posts
    q = filter.q or ""
    query = select(Post).where(Post.title.contains(q) | Post.description.contains(q))

    # Filtra por intervalo de tempo
    if filter.start_date and filter.end_date:
        query = query.where(
            Post.date_published.between(filter.start_date, filter.end_date)
        )

    # Ordena por coluna
    if filter.order == "asc":
        query = query.order_by(filter.sort_by)
    else:
        query = query.order_by(desc(filter.sort_by))

    # Aplica paginação
    offset = (filter.p - 1) * filter.pp
    posts = session.scalars(query.offset(offset).limit(filter.pp))

    return {"data": posts.all()}


@router.get("/sources", response_model=ItemList)
def read_sources(session: DBSession):
    sources = session.scalars(select(Post.source).distinct())

    return {"data": sources.all()}


@router.get("/subjects", response_model=ItemList)
def read_subjects(session: DBSession):
    subjects = session.scalars(
        select(Post.type).where(Post.type.is_not(None)).distinct()
    )

    return {"data": subjects.all()}


@router.get("/stats", response_model=Stats)
def read_stats(session: DBSession):
    total_news = session.scalar(select(func.count(Post.id)))

    today = date.today()
    today_news = session.scalar(
        select(func.count(Post.id)).where(
            Post.date_published.between(today, today + timedelta(days=1))
        )
    )

    news_by_subjects = (
        session.execute(
            select(func.count(Post.id), Post.type.label("subject"))
            .where(Post.type.is_not(None))
            .group_by(Post.type)
        )
        .mappings()
        .all()
    )

    news_by_subjects = [SubjectCount.model_validate(data) for data in news_by_subjects]

    news_by_sources = (
        session.execute(select(func.count(Post.id), Post.source).group_by(Post.source))
        .mappings()
        .all()
    )
    news_by_sources = [SourceCount.model_validate(data) for data in news_by_sources]

    return {
        "total_news": total_news,
        "today": today_news,
        "news_by_subjects": news_by_subjects,
        "news_by_sources": news_by_sources,
    }
