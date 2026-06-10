from datetime import datetime

from pydantic import BaseModel


class AuditInfo(BaseModel):
    """監査用のレスポンスモデル

    Arguments:
    - created_at: 作成日時
    - created_by: 作成者
    - last_updated_at: 最終更新日時
    - last_updated_by: 最終更新者
    """

    created_at: datetime
    created_by: str
    last_updated_at: datetime
    last_updated_by: str


class MetaInfo(AuditInfo):
    """メタ用のレスポンスモデル

    Arguments:
    - deleted_at: 削除日時
    - deleted_by: 削除者
    - version: 楽観ロックのバージョン番号
    """

    deleted_at: datetime | None
    deleted_by: str | None
    version: int
