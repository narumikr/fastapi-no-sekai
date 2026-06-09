from app.application.commands.artist_command import CreateArtistCommand
from app.application.dtos.artist_dtos import ArtistDto
from app.application.mappers.artist_mapper import ArtistMapper
from app.application.unit_of_work import UnitOfWork
from app.contexts.artist.artist_models import Artist


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
        new_artist = Artist.create_new_artist(
            artist_name=artist.artist_name,
            unit_name=artist.unit_name,
        )
        try:
            saved_artist = self.unit_of_work.artists.save_artist(new_artist)
            self.unit_of_work.commit()
        except Exception:
            self.unit_of_work.rollback()
            raise

        return ArtistMapper.to_artist_dto(saved_artist)
