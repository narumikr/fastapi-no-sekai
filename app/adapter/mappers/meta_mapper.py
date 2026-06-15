from app.adapter.infrastructure.db.base_entity import BaseEntity
from app.contexts.shared.meta_models import MetaModel


class MetaMapper:
    """ORMエンティティのメタ情報をドメインモデルへ変換するクラス"""

    @staticmethod
    def to_meta_model(entity: BaseEntity) -> MetaModel:
        """ORMエンティティからMetaModelを生成する"""
        return MetaModel(
            created_at=entity.created_at,
            created_by=entity.created_by,
            last_updated_at=entity.last_updated_at,
            last_updated_by=entity.last_updated_by,
            deleted_at=entity.deleted_at,
            deleted_by=entity.deleted_by,
            version=entity.version,
        )
