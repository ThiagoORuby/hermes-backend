from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from core.database import get_session
from core.models import Post


def test_get_session():
    session = next(get_session())

    assert type(session) is Session


def test_create_post(session: Session):
    new_post = Post(
        image_url="image_url",
        title="A test post",
        description="Description of a test post",
        url="url",
        date_published=datetime.today(),
        source="test",
        type="test",
    )

    session.add(new_post)
    session.commit()

    post = session.scalar(select(Post).where(Post.title == "A test post"))

    assert post is not None
    assert post.url == "url"
