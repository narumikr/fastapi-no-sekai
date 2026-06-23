from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """SQLAlchemy の Declarative Base クラス"""

    pass


class BaseEntity(Base):
    __abstract__ = True

    """ORM エンティティの基底クラス

    - created_at: 作成日時
    - created_by: 作成者
    - last_updated_at: 最終更新日時
    - last_updated_by: 最終更新者
    - deleted_at: 削除日時
    - deleted_by: 削除者
    - version: 楽観ロックのバージョン番号
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    created_by: Mapped[str] = mapped_column(
        String(50), default="system", nullable=False
    )

    last_updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    last_updated_by: Mapped[str] = mapped_column(
        String(50), default="system", onupdate="system", nullable=False
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    deleted_by: Mapped[str | None] = mapped_column(String(50), nullable=True)

    version: Mapped[int] = mapped_column(
        Integer,
        server_default=text("0"),
        nullable=False,
    )
    __mapper_args__ = {"version_id_col": version}
