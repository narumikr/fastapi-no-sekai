from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.core.config import get_timezone
from app.core.database import Base


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
        DateTime, default=lambda: datetime.now(get_timezone()), nullable=False
    )
    created_by = Column(String(50), default="system", nullable=False)

    last_updated_at = Column(
        DateTime,
        default=lambda: datetime.now(get_timezone()),
        onupdate=lambda: datetime.now(get_timezone()),
        nullable=False,
    )
    last_updated_by = Column(
        String(50), default="system", onupdate="system", nullable=False
    )

    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(String(50), nullable=True)

    version = Column(
        Integer,
        default=0,
        nullable=False,
    )
    __mapper_args__ = {"version_id_col": version}
