from app.application.dtos.artist_dtos import ArtistDto
from app.application.dtos.base_dtos import MetaDto
from app.contexts.artist.artist_models import Artist


class ArtistMapper:
    """ドメインモデルから内部DTOへの変換などアウトバウンドマッピングを行うクラス"""

    @staticmethod
    def to_artist_dto(artist: Artist) -> ArtistDto:
        """ドメインモデルをアーティストの内部DTOに変換"""

        assert artist.id is not None, "自動採番されているのでIDは存在する。"
        assert artist.meta_info is not None, (
            "メタ情報も自動でセットされるので存在する。"
        )

        return ArtistDto(
            id=artist.id,
            artist_name=artist.artist_name,
            unit_name=artist.unit_name,
            meta_info=MetaDto(
                created_at=artist.meta_info.created_at,
                created_by=artist.meta_info.created_by,
                last_updated_at=artist.meta_info.last_updated_at,
                last_updated_by=artist.meta_info.last_updated_by,
                deleted_at=artist.meta_info.deleted_at,
                deleted_by=artist.meta_info.deleted_by,
                version=artist.meta_info.version,
            ),
        )
