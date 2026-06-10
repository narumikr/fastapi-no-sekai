from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.adapter.infrastructure.db.artist_entity import ArtistEntity
from app.contexts.artist.artist_exception import ArtistDuplicateNameException, ArtistError
from app.contexts.artist.artist_models import Artist
from app.contexts.artist.artist_repository import ArtistRepository
from app.contexts.shared.meta_models import MetaModel


class ArtistRepositoryImpl(ArtistRepository):
    """アーティストリポジトリの実装クラス

    Description:
    - アーティストの永続化や取得に関する具体的な実装を提供するクラス
    """

    def __init__(self, db: Session):
        self.db = db

    def save_artist(self, artist: Artist) -> Artist:
        """アーティストを永続化するための具体的な実装

        Args:
        - artist: Artist - 永続化するアーティストのドメインモデル

        Returns:
        - Artist: 永続化されたアーティストのドメインモデル
        """
        artist_entity = ArtistEntity(
            artist_name=artist.artist_name,
            unit_name=artist.unit_name,
        )
        self.db.add(artist_entity)
        try:
            self.db.flush()
        except IntegrityError:
            raise ArtistDuplicateNameException(ArtistError.DUPLICATE_NAME)

        meta_info = MetaModel(
            created_at=artist_entity.created_at,
            created_by=artist_entity.created_by,
            last_updated_at=artist_entity.last_updated_at,
            last_updated_by=artist_entity.last_updated_by,
            deleted_at=artist_entity.deleted_at,
            deleted_by=artist_entity.deleted_by,
            version=artist_entity.version,
        )

        return Artist(
            id=artist_entity.id,
            artist_name=artist_entity.artist_name,
            unit_name=artist_entity.unit_name,
            meta_info=meta_info,
        )
