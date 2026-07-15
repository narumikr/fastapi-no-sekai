import logging
from datetime import datetime

import pytest

from app.application.commands.artist_command import CreateArtistCommand
from app.application.dtos.base_dtos import MetaDto
from app.application.unit_of_work import UnitOfWork
from app.application.usecases.artist_usecase import ArtistUseCase
from app.contexts.artist.artist_models import Artist
from app.contexts.artist.artist_repository import ArtistRepository

_SAVED_ID = 42


class _FakeArtistRepository(ArtistRepository):
    def save_artist(self, artist: Artist) -> Artist:
        return Artist(
            id=_SAVED_ID,
            artist_name=artist.artist_name,
            unit_name=artist.unit_name,
            meta_info=MetaDto(
                created_at=datetime(2026, 7, 10),
                created_by="system",
                last_updated_at=datetime(2026, 7, 10),
                last_updated_by="system",
                deleted_at=None,
                deleted_by=None,
                version=1,
            ),
        )


class _FakeUnitOfWork(UnitOfWork):
    def __init__(self):
        self.artists = _FakeArtistRepository()
        self.commit_called = False

    def commit(self) -> None:
        self.commit_called = True

    def rollback(self) -> None:
        pass


class TestCreateArtistUseCaseLogging:
    def test_登録開始時に_INFO_ログが出力される(
        self, app_caplog: pytest.LogCaptureFixture
    ):
        usecase = ArtistUseCase(_FakeUnitOfWork())
        command = CreateArtistCommand(artist_name="Leo/need", unit_name="Leo/need")

        usecase.create_artist_usecase(command)

        start_logs = [
            r
            for r in app_caplog.records
            if r.levelno == logging.INFO
            and "開始" in r.getMessage()
            and "Leo/need" in r.getMessage()
        ]
        assert len(start_logs) == 1

    def test_登録完了時に_保存された_ID_を含む_INFO_ログが出力される(
        self, app_caplog: pytest.LogCaptureFixture
    ):
        usecase = ArtistUseCase(_FakeUnitOfWork())
        command = CreateArtistCommand(artist_name="Leo/need")

        usecase.create_artist_usecase(command)

        complete_logs = [
            r
            for r in app_caplog.records
            if r.levelno == logging.INFO
            and "完了" in r.getMessage()
            and str(_SAVED_ID) in r.getMessage()
        ]
        assert len(complete_logs) == 1

    def test_開始ログにユニット名も含まれる(self, app_caplog: pytest.LogCaptureFixture):
        usecase = ArtistUseCase(_FakeUnitOfWork())
        command = CreateArtistCommand(artist_name="星乃一歌", unit_name="Leo/need")

        usecase.create_artist_usecase(command)

        start_msg = next(
            r.getMessage()
            for r in app_caplog.records
            if r.levelno == logging.INFO and "開始" in r.getMessage()
        )
        assert "星乃一歌" in start_msg
        assert "Leo/need" in start_msg

    def test_ドメイン例外送出時は完了ログが出力されない(
        self, app_caplog: pytest.LogCaptureFixture
    ):
        from app.contexts.artist.artist_exception import ArtistBadRequestException

        usecase = ArtistUseCase(_FakeUnitOfWork())
        command = CreateArtistCommand(artist_name="")

        with pytest.raises(ArtistBadRequestException):
            usecase.create_artist_usecase(command)

        complete_logs = [
            r
            for r in app_caplog.records
            if r.levelno == logging.INFO and "完了" in r.getMessage()
        ]
        assert complete_logs == []
