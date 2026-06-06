from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.adapter.infrastructure.artist_repository_impl import ArtistRepositoryImpl
from app.adapter.mappers.artist_mapper import ArtistMapper
from app.adapter.schemas.artist_schema import ArtistResponse, CreateArtistRequest
from app.application.usecases.artist_usecase import ArtistUseCase
from app.core.database import get_db

router = APIRouter()


@router.post("", response_model=ArtistResponse, status_code=201)
async def create_artist(
    request: CreateArtistRequest, db: Session = Depends(get_db)
) -> ArtistResponse:
    """新規アーティストの登録エンドポイント

    Args:
    - request: CreateArtistRequest - アーティスト作成のためのリクエストボディ

    Returns:
    - ArtistResponse: 作成されたアーティストの情報を含むレスポンス
    """
    repository = ArtistRepositoryImpl(db=db)
    usecase = ArtistUseCase(artist_repository=repository)

    command = ArtistMapper.to_create_command(request)
    artist_dto = usecase.create_artist_usecase(command)

    return ArtistMapper.to_artist_response(artist_dto)
