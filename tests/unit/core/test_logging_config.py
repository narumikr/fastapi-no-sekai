import importlib
import logging

import pytest

from app.core import logging_config
from app.core.logging_config import LOGGING_CONFIG, setup_logging


class TestLoggingConfigDict:
    def test_フォーマット文字列に必要な要素が含まれる(self):
        fmt = LOGGING_CONFIG["formatters"]["default"]["format"]
        assert "%(asctime)s" in fmt
        assert "%(levelname)s" in fmt
        assert "%(name)s" in fmt
        assert "%(message)s" in fmt

    def test_app_ロガーは_propagate_False_で二重出力を防ぐ(self):
        assert LOGGING_CONFIG["loggers"]["app"]["propagate"] is False

    @pytest.mark.parametrize(
        "logger_name", ["uvicorn", "uvicorn.error", "uvicorn.access"]
    )
    def test_uvicorn_系ロガーも_propagate_False(self, logger_name: str):
        assert LOGGING_CONFIG["loggers"][logger_name]["propagate"] is False

    def test_app_ロガーのレベルは_LOG_LEVEL_変数と一致する(self):
        assert LOGGING_CONFIG["loggers"]["app"]["level"] == logging_config.LOG_LEVEL


class TestLogLevelEnv:
    """LOG_LEVEL 環境変数によりロガーレベルが切り替わることを確認する

    Description:
    - モジュール import 時に環境変数を読むため、`importlib.reload` で再評価する。
    - テスト後は環境変数をデフォルトに戻し、モジュールを再ロードして
      他テストへの影響を排除する。
    """

    def test_LOG_LEVEL_未設定時のデフォルトは_INFO(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        monkeypatch.delenv("LOG_LEVEL", raising=False)
        try:
            importlib.reload(logging_config)
            assert logging_config.LOG_LEVEL == "INFO"
        finally:
            monkeypatch.delenv("LOG_LEVEL", raising=False)
            importlib.reload(logging_config)

    def test_LOG_LEVEL_環境変数でレベルが変更できる(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        monkeypatch.setenv("LOG_LEVEL", "debug")
        try:
            importlib.reload(logging_config)
            assert logging_config.LOG_LEVEL == "DEBUG"
            assert logging_config.LOGGING_CONFIG["loggers"]["app"]["level"] == "DEBUG"
        finally:
            monkeypatch.delenv("LOG_LEVEL", raising=False)
            importlib.reload(logging_config)


class TestSetupLogging:
    def test_setup_logging_で_app_ロガーに_StreamHandler_が付与される(self):
        setup_logging()
        app_logger = logging.getLogger("app")
        assert any(isinstance(h, logging.StreamHandler) for h in app_logger.handlers)

    def test_setup_logging_で_フォーマッタが適用される(self):
        setup_logging()
        app_logger = logging.getLogger("app")
        stream_handlers = [
            h for h in app_logger.handlers if isinstance(h, logging.StreamHandler)
        ]
        assert stream_handlers, "app ロガーに StreamHandler が付与されていない"
        formatter = stream_handlers[0].formatter
        assert formatter is not None
        assert formatter._fmt == LOGGING_CONFIG["formatters"]["default"]["format"]
