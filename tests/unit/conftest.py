"""単体テスト共通の fixture 定義"""

import logging
from collections.abc import Generator

import pytest


@pytest.fixture
def app_caplog(
    caplog: pytest.LogCaptureFixture,
) -> Generator[pytest.LogCaptureFixture]:
    """`app.*` 配下のロガーからログを確実に捕捉する caplog ラッパー

    Description:
    - 本番設定 (`setup_logging`) では `app` ロガーの propagate=False にしているため、
      root ロガー経由の caplog では拾えないケースがある。
    - caplog.handler を `app` ロガーに直接付与することで、
      本番の propagate 設定を壊さずにテストからログを検証できるようにする。
    """
    app_logger = logging.getLogger("app")
    original_propagate = app_logger.propagate
    app_logger.addHandler(caplog.handler)
    app_logger.propagate = False
    caplog.set_level(logging.DEBUG, logger="app")
    try:
        yield caplog
    finally:
        app_logger.removeHandler(caplog.handler)
        app_logger.propagate = original_propagate
