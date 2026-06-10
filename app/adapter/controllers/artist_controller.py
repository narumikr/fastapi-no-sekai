from fastapi import APIRouter, Depends

from app.adapter.dependencies import get_artist_usecase
from app.adapter.mappers.artist_mapper import ArtistMapper
from app.adapter.schemas.artist_schema import ArtistResponse, CreateArtistRequest
from app.application.usecases.artist_usecase import ArtistUseCase

router = APIRouter()


@router.post("", response_model=ArtistResponse, status_code=201)
async def create_artist(
    request: CreateArtistRequest,
    usecase: ArtistUseCase = Depends(get_artist_usecase),
) -> ArtistResponse:
    """新規アーティストの登録エンドポイント

    Args:
    - request: CreateArtistRequest - アーティスト作成のためのリクエストボディ

    Returns:
    - ArtistResponse: 作成されたアーティストの情報を含むレスポンス
    """
    command = ArtistMapper.to_create_command(request)
    artist_dto = usecase.create_artist_usecase(command)

    return ArtistMapper.to_artist_response(artist_dto)
