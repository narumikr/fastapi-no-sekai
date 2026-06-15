import os
from collections.abc import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import TIMEZONE_NAME

load_dotenv()

DATABASE_URL = (
    f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}"
    f"@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
)

engine = create_engine(
    DATABASE_URL,
    connect_args={"options": f"-c timezone={TIMEZONE_NAME}"},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session]:
    """FastAPI の Depends で使う DB セッションの生成と後処理

    トランザクション管理の主責任は UnitOfWork が持つ。
    セッション close 時の暗黙 rollback は予期しない例外に対するセーフティネット。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
