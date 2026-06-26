"""IT テスト共通の fixture 定義

テスト DB は Testcontainers で起動した PostgreSQL を使用し、
ローカル常設 DB には依存しない。

- セッション開始時に PostgreSQL コンテナを起動し、接続情報を環境変数にセット
- `app.core.database` はモジュール import 時に環境変数からエンジンを構築するため、
  接続情報のセットは `app` を import するより前に行う必要がある
- テストごとに TRUNCATE して状態をリセットし、実行順序への依存を排除する
"""

import os
from collections.abc import Generator
from pathlib import Path

import pytest
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from testcontainers.postgres import PostgresContainer


def _configure_docker_host_for_colima() -> None:
    """colima 利用時に DOCKER_HOST を補完する

    testcontainers (docker-py) は Docker context を見ず、
    DOCKER_HOST もしくは /var/run/docker.sock を参照するため、
    colima の socket を明示する必要がある。
    Ryuk コンテナ側からは /var/run/docker.sock が見えるので
    TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE も合わせて指定する。
    """
    if os.environ.get("DOCKER_HOST"):
        return
    colima_socket = Path.home() / ".colima" / "default" / "docker.sock"
    if colima_socket.exists():
        os.environ["DOCKER_HOST"] = f"unix://{colima_socket}"
        os.environ.setdefault(
            "TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE", "/var/run/docker.sock"
        )


@pytest.fixture(scope="session", autouse=True)
def _postgres_container() -> Generator[PostgresContainer]:
    """テスト用 PostgreSQL コンテナをセッション全体で起動する"""
    _configure_docker_host_for_colima()
    with PostgresContainer("postgres:16") as container:
        os.environ["DATABASE_HOST"] = container.get_container_host_ip()
        os.environ["DATABASE_PORT"] = str(container.get_exposed_port(5432))
        os.environ["DATABASE_USER"] = container.username
        os.environ["DATABASE_PASSWORD"] = container.password
        os.environ["DATABASE_NAME"] = container.dbname
        yield container


@pytest.fixture(scope="session")
def _engine(_postgres_container: PostgresContainer) -> Engine:
    """テスト DB に接続するエンジン

    `Base.metadata` に ORM エンティティを登録した上で、
    テーブルを作成しておく。
    """
    import app.adapter.infrastructure.db  # noqa: F401
    from app.adapter.infrastructure.db.base_entity import Base

    url = (
        f"postgresql://{os.environ['DATABASE_USER']}:{os.environ['DATABASE_PASSWORD']}"
        f"@{os.environ['DATABASE_HOST']}:{os.environ['DATABASE_PORT']}"
        f"/{os.environ['DATABASE_NAME']}"
    )
    engine = create_engine(url)
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope="session")
def _session_factory(_engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(autocommit=False, autoflush=False, bind=_engine)


@pytest.fixture(autouse=True)
def _truncate_tables(_engine: Engine) -> Generator[None]:
    """テストごとにテーブルを TRUNCATE して独立性を担保する"""
    yield
    with _engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE artists RESTART IDENTITY CASCADE"))
        conn.commit()


@pytest.fixture
def db_session(_session_factory: sessionmaker[Session]) -> Generator[Session]:
    session = _session_factory()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(_session_factory: sessionmaker[Session]) -> Generator:
    from fastapi.testclient import TestClient

    from app.core.database import get_db
    from app.main import app

    def _override_get_db() -> Generator[Session]:
        session = _session_factory()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
