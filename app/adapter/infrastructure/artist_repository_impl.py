from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.adapter.infrastructure.db.artist_entity import ArtistEntity
from app.adapter.mappers.meta_mapper import MetaMapper
from app.contexts.artist.artist_exception import ArtistDuplicateNameException, ArtistError
from app.contexts.artist.artist_models import Artist
from app.contexts.artist.artist_repository import ArtistRepository


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

        self.db.refresh(artist_entity)
        meta_info = MetaMapper.to_meta_model(artist_entity)

        return Artist(
            id=artist_entity.id,
            artist_name=artist_entity.artist_name,
            unit_name=artist_entity.unit_name,
            meta_info=meta_info,
        )
