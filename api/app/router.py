from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.app.schemas import PostList
from core.database import get_session
from core.models import Post

router = APIRouter(prefix="/api/v1", tags=["api_v1"])

DBSession = Annotated[Session, Depends(get_session)]


@router.get("/posts", response_model=PostList)
def read_posts(session: DBSession):

    posts = session.scalars(select(Post)).all()

    return {"data": posts}
