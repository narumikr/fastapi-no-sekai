import os
from collections.abc import Generator
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_timezone

load_dotenv()

DATABASE_URL = (
    f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}"
    f"@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class BaseEntity(Base):
    __abstract__ = True

    """ドメインエンティティの基底クラス

    - created_at: 作成日時
    - created_by: 作成者
    - last_updated_at: 最終更新日時
    - last_updated_by: 最終更新者
    - deleted_at: 削除日時
    - deleted_by: 削除者
    - version: 楽観ロックのバージョン番号
    """

    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(get_timezone()), nullable=False
    )
    created_by = Column(String(50), default="system", nullable=False)

    last_updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(get_timezone()),
        onupdate=lambda: datetime.now(get_timezone()),
        nullable=False,
    )
    last_updated_by = Column(
        String(50), default="system", onupdate="system", nullable=False
    )

    deleted_at = Column(DateTime(timezone=True), nullable=True)
    deleted_by = Column(String(50), nullable=True)

    version = Column(
        Integer,
        default=0,
        nullable=False,
    )
    __mapper_args__ = {"version_id_col": version}


def get_db() -> Generator[Session]:
    """FastAPI の Depends で使う DB セッションの生成と後処理"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
