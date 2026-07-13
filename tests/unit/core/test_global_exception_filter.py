import asyncio
import logging
from unittest.mock import Mock

import pytest

from app.contexts.artist.artist_exception import (
    ArtistBadRequestException,
    ArtistDuplicateNameException,
    ArtistError,
)
from app.contexts.shared.exceptions import BussinessException
from app.core.global_exception_filter import (
    business_exception_handler,
    unhandled_exception_handler,
)


def _make_request(method: str = "POST", path: str = "/artists") -> Mock:
    request = Mock()
    request.method = method
    request.url.path = path
    return request


class TestBusinessExceptionLogging:
    def test_業務例外は_WARNING_レベルで記録される(
        self, app_caplog: pytest.LogCaptureFixture
    ):
        request = _make_request()
        exc = ArtistBadRequestException(ArtistError.NAME_REQUIRED)

        asyncio.run(business_exception_handler(request, exc))

        warnings = [r for r in app_caplog.records if r.levelno == logging.WARNING]
        assert len(warnings) == 1

    def test_業務例外のログには_メソッド_パス_ステータス_コード_メッセージが含まれる(
        self, app_caplog: pytest.LogCaptureFixture
    ):
        request = _make_request(method="POST", path="/artists")
        exc = ArtistBadRequestException(ArtistError.NAME_REQUIRED)

        asyncio.run(business_exception_handler(request, exc))

        msg = next(
            r.getMessage()
            for r in app_caplog.records
            if r.levelno == logging.WARNING
        )
        assert "POST" in msg
        assert "/artists" in msg
        assert "400" in msg
        assert "NAME_REQUIRED" in msg
        assert ArtistError.NAME_REQUIRED.value in msg

    def test_重複エラーはステータス_409_として記録される(
        self, app_caplog: pytest.LogCaptureFixture
    ):
        request = _make_request()
        exc = ArtistDuplicateNameException(ArtistError.DUPLICATE_NAME)

        asyncio.run(business_exception_handler(request, exc))

        msg = next(
            r.getMessage()
            for r in app_caplog.records
            if r.levelno == logging.WARNING
        )
        assert "409" in msg
        assert "DUPLICATE_NAME" in msg

    def test_マップ未登録の業務例外はステータス_400_として記録される(
        self, app_caplog: pytest.LogCaptureFixture
    ):
        class UnknownBusinessError(BussinessException):
            pass

        request = _make_request()
        exc = UnknownBusinessError(code="UNKNOWN", message="unknown error")

        asyncio.run(business_exception_handler(request, exc))

        msg = next(
            r.getMessage()
            for r in app_caplog.records
            if r.levelno == logging.WARNING
        )
        assert "400" in msg


class TestUnhandledExceptionLogging:
    def test_想定外例外は_ERROR_レベルで記録される(
        self, app_caplog: pytest.LogCaptureFixture
    ):
        request = _make_request()
        exc = RuntimeError("boom!")

        asyncio.run(unhandled_exception_handler(request, exc))

        errors = [r for r in app_caplog.records if r.levelno == logging.ERROR]
        assert len(errors) == 1

    def test_想定外例外のログには_メソッド_パスが含まれる(
        self, app_caplog: pytest.LogCaptureFixture
    ):
        request = _make_request(method="GET", path="/artists/42")
        exc = RuntimeError("boom!")

        asyncio.run(unhandled_exception_handler(request, exc))

        msg = next(
            r.getMessage() for r in app_caplog.records if r.levelno == logging.ERROR
        )
        assert "GET" in msg
        assert "/artists/42" in msg

    def test_想定外例外はトレースバック情報を含めて記録される(
        self, app_caplog: pytest.LogCaptureFixture
    ):
        request = _make_request()
        exc = RuntimeError("boom!")

        asyncio.run(unhandled_exception_handler(request, exc))

        record = next(r for r in app_caplog.records if r.levelno == logging.ERROR)
        assert record.exc_info is not None
        assert record.exc_info[0] is RuntimeError
