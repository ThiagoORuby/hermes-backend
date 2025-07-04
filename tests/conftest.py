import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from api.app import app
from core.database import get_session
from core.models import table_registry


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app.app) as client:
        app.app.dependency_overrides[get_session] = get_session_override
        yield client

    app.app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
