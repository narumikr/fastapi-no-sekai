import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

import app.adapter.infrastructure.db  # noqa: F401 - ORM エンティティを Base に登録
from app.adapter.infrastructure.db.base_entity import Base
from app.core.database import get_db
from app.main import app

load_dotenv()

_engine = create_engine(
    f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}"
    f"@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}",
)
_SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=_engine)
    yield


@pytest.fixture(autouse=True)
def truncate_tables(setup_database):
    yield
    with _engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE artists RESTART IDENTITY CASCADE"))
        conn.commit()


@pytest.fixture
def db_session(truncate_tables):
    session = _SessionFactory()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(truncate_tables):
    def _override_get_db():
        session = _SessionFactory()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
