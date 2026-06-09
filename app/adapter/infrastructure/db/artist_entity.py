from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import BaseEntity


class ArtistEntity(BaseEntity):
    """アーティストエンティティクラス

    Attributes:
    - id: アーティストID
    - artist_name: アーティスト名
    - unit_name: ユニット名（任意）
    - created_at: 作成日時
    - created_by: 作成者
    - last_updated_at: 最終更新日時
    - last_updated_by: 最終更新者
    - deleted_at: 削除日時
    - deleted_by: 削除者
    - version: 楽観ロックのバージョン番号
    """

    __tablename__ = "artists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    artist_name: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )

    unit_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
