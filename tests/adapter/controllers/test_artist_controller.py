from unittest.mock import MagicMock

from app.adapter.dependencies import get_artist_usecase
from app.application.usecases.artist_usecase import ArtistUseCase
from app.contexts.artist.artist_exception import (
    ArtistBadRequestException,
    ArtistDuplicateNameException,
    ArtistError,
)
from app.main import app


def test_create_artist_duplicate_name_returns_409(client):
    mock = MagicMock(spec=ArtistUseCase)
    mock.create_artist_usecase.side_effect = ArtistDuplicateNameException(
        ArtistError.DUPLICATE_NAME
    )
    app.dependency_overrides[get_artist_usecase] = lambda: mock

    response = client.post("/artists", json={"artist_name": "Leo/need"})

    assert response.status_code == 409
    body = response.json()
    assert body["code"] == "DUPLICATE_NAME"
    assert body["message"] == "同じアーティスト名が既に存在しています。"
    assert body["details"] == []


def test_create_artist_bad_request_returns_400(client):
    mock = MagicMock(spec=ArtistUseCase)
    mock.create_artist_usecase.side_effect = ArtistBadRequestException(
        ArtistError.NAME_REQUIRED
    )
    app.dependency_overrides[get_artist_usecase] = lambda: mock

    response = client.post("/artists", json={"artist_name": ""})

    assert response.status_code == 400
    body = response.json()
    assert body["code"] == "NAME_REQUIRED"
    assert body["message"] == "アーティスト名は必須です。"
    assert body["details"] == []


def test_create_artist_unhandled_exception_returns_500(client):
    mock = MagicMock(spec=ArtistUseCase)
    mock.create_artist_usecase.side_effect = RuntimeError("unexpected error")
    app.dependency_overrides[get_artist_usecase] = lambda: mock

    response = client.post("/artists", json={"artist_name": "Leo/need"})

    assert response.status_code == 500
    body = response.json()
    assert body["code"] == "INTERNAL_SERVER_ERROR"
    assert body["message"] == "予期しないエラーが発生しました。"
    assert body["details"] == []
