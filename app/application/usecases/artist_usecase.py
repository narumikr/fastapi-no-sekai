from app.application.commands.artist_command import CreateArtistCommand
from app.application.dtos.artist_dtos import ArtistDto
from app.application.mappers.artist_mapper import ArtistMapper
from app.contexts.artist.artist_models import Artist
from app.contexts.artist.artist_repository import ArtistRepository


class ArtistUseCase:
    """アーティストに関するユースケースを定義するクラス

    Description:
    - create_artist_usecase: 新規アーティストの登録
    """

    def __init__(self, artist_repository: ArtistRepository):
        self.artist_repository = artist_repository
        self.db = artist_repository.db

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
        saved_artist = self.artist_repository.save_artist(new_artist)
        self.db.commit()

        return ArtistMapper.to_artist_dto(saved_artist)
