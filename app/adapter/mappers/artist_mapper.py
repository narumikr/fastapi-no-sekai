from app.adapter.schemas.artist_schema import ArtistResponse, CreateArtistRequest
from app.application.commands.artist_command import CreateArtistCommand
from app.application.dtos.artist_dtos import ArtistDto
from app.adapter.schemas.meta_schema import MetaInfo


class ArtistMapper:
    """APIリクエストから内部DTOへの変換などインバウンドマッピングを行うクラス"""

    @staticmethod
    def to_create_command(request: CreateArtistRequest) -> CreateArtistCommand:
        """APIリクエストをアーティストの内部DTOに変換"""
        return CreateArtistCommand(
            artist_name=request.artist_name,
            unit_name=request.unit_name,
        )

    @staticmethod
    def to_artist_response(dto: ArtistDto) -> ArtistResponse:
        """アーティストの内部DTOをAPIレスポンスに変換"""
        return ArtistResponse(
            id=dto.id,
            artist_name=dto.artist_name,
            unit_name=dto.unit_name,
            meta_info=MetaInfo(
                created_at=dto.meta_info.created_at,
                created_by=dto.meta_info.created_by,
                last_updated_at=dto.meta_info.last_updated_at,
                last_updated_by=dto.meta_info.last_updated_by,
                deleted_at=dto.meta_info.deleted_at,
                deleted_by=dto.meta_info.deleted_by,
                version=dto.meta_info.version,
            ),
        )
