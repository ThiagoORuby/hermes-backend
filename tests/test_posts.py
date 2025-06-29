from factory.base import Factory
from factory.faker import Faker
from factory.fuzzy import FuzzyChoice
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from core.models import Post

test_subjects = ["esportes", "filmes", "novelas"]


class PostFactory(Factory):
    class Meta:  # type: ignore
        model = Post

    title = Faker("text")
    description = Faker("text")
    image_url = Faker("image_url")
    url = Faker("url")
    date_published = Faker("date_time")
    source = FuzzyChoice(["uol", "g1"])
    type = FuzzyChoice(test_subjects)


def test_read_all_posts(session: Session, client: TestClient):
    expected = 5
    session.add_all(PostFactory.create_batch(5))
    session.commit()

    response = client.get("/api/v1/posts/")

    assert len(response.json()["data"]) == expected


def test_read_all_sources(session: Session, client: TestClient):
    session.add_all(PostFactory.create_batch(2, type="g1"))
    session.add_all(PostFactory.create_batch(2, type="uol"))
    session.commit()

    response = client.get("/api/v1/sources/")

    assert sorted(response.json()["data"]) == ["g1", "uol"]


def test_read_all_subjects(session: Session, client: TestClient):
    session.add_all(PostFactory.create_batch(5))

    response = client.get("/api/v1/subjects/")

    assert set.issubset(set(response.json()["data"]), set(test_subjects))


# TODO: testes para filtros e stats
