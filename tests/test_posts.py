import datetime

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
    session.add_all(PostFactory.create_batch(2, source="g1"))
    session.commit()
    session.add_all(PostFactory.create_batch(2, source="uol"))
    session.commit()

    response = client.get("/api/v1/sources/")

    assert sorted(response.json()["data"]) == ["g1", "uol"]


def test_read_all_subjects(session: Session, client: TestClient):
    session.add_all(PostFactory.create_batch(5))
    session.commit()

    response = client.get("/api/v1/subjects/")

    assert set.issubset(set(response.json()["data"]), set(test_subjects))


def test_read_posts_filter_q_query(session: Session, client: TestClient):
    expected = 5
    session.add_all(PostFactory.create_batch(5, title="Title Filter"))
    session.commit()

    response = client.get("/api/v1/posts/?q=Title Filter")

    assert len(response.json()["data"]) == expected


def test_read_posts_filter_asc_order(session: Session, client: TestClient):
    data = PostFactory.create_batch(
        5,
        date_published=Faker(
            "date_between",
            start_date=datetime.date(2025, 1, 1),
            end_date=datetime.date(2025, 5, 1),
        ),
    )

    session.add_all(data)
    session.commit()

    response = client.get("/api/v1/posts/?order=asc")

    sorted_data = sorted(data, key=lambda d: d.date_published)

    assert [d["datePublished"] for d in response.json()["data"]] == [
        d.date_published.isoformat() for d in sorted_data
    ]


def test_read_posts_filter_desc_order(session: Session, client: TestClient):
    data = PostFactory.create_batch(
        5,
        date_published=Faker(
            "date_between",
            start_date=datetime.date(2025, 1, 1),
            end_date=datetime.date(2025, 5, 1),
        ),
    )

    session.add_all(data)
    session.commit()

    response = client.get("/api/v1/posts/?order=desc")

    sorted_data = sorted(data, key=lambda d: d.date_published, reverse=True)

    assert [d["datePublished"] for d in response.json()["data"]] == [
        d.date_published.isoformat() for d in sorted_data
    ]


def test_read_posts_filter_date_interval(session: Session, client: TestClient):
    expected = 5
    session.add_all(
        PostFactory.create_batch(
            expected,
            date_published=Faker(
                "date_between",
                start_date=datetime.date(2025, 1, 1),
                end_date=datetime.date(2025, 5, 1),
            ),
        )
    )
    session.commit()
    session.add_all(
        PostFactory.create_batch(
            5,
            date_published=Faker(
                "date_between",
                start_date="-3y",
                end_date="-2y",
            ),
        )
    )
    session.commit()

    response = client.get("/api/v1/posts/?start_date=2025-01-01&end_date=2025-05-01")

    assert len(response.json()["data"]) == expected


def test_read_stats(session: Session, client: TestClient):
    session.add_all(
        PostFactory.create_batch(
            5, date_published=datetime.datetime.today(), source="uol", type="política"
        )
    )
    session.commit()

    session.add_all(
        PostFactory.create_batch(
            5,
            date_published=Faker("date_time", end_datetime="-1w"),
            source="g1",
            type="esportes",
        )
    )
    session.commit()

    expected_results = {
        "totalNews": 10,
        "today": 5,
        "newsBySubjects": [
            {"subject": "esportes", "count": 5},
            {
                "subject": "política",
                "count": 5,
            },
        ],
        "newsBySources": [
            {"source": "g1", "count": 5},
            {
                "source": "uol",
                "count": 5,
            },
        ],
    }

    response = client.get("/api/v1/stats")

    assert response.json() == expected_results
