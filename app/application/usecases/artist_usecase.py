import logging

from app.application.commands.artist_command import CreateArtistCommand
from app.application.dtos.artist_dtos import ArtistDto
from app.application.mappers.artist_mapper import ArtistMapper
from app.application.unit_of_work import UnitOfWork
from app.contexts.artist.artist_models import Artist

logger = logging.getLogger(__name__)


class ArtistUseCase:
    """アーティストに関するユースケースを定義するクラス

    Description:
    - create_artist_usecase: 新規アーティストの登録
    """

    def __init__(self, unit_of_work: UnitOfWork):
        self.unit_of_work = unit_of_work

    def create_artist_usecase(self, artist: CreateArtistCommand) -> ArtistDto:
        """新規アーティストの登録ユースケース

        Args:
        - artist: CreateArtistCommand - 登録するアーティストのコマンド

        Returns:
        - ArtistDto: 登録されたアーティストのDTO
        """
        logger.info(
            "アーティスト登録を開始します: artist_name=%s unit_name=%s",
            artist.artist_name,
            artist.unit_name,
        )
        new_artist = Artist.create_new_artist(
            artist_name=artist.artist_name,
            unit_name=artist.unit_name,
        )
        saved_artist = self.unit_of_work.artists.save_artist(new_artist)
        self.unit_of_work.commit()
        logger.info("アーティスト登録が完了しました: id=%s", saved_artist.id)
        return ArtistMapper.to_artist_dto(saved_artist)
