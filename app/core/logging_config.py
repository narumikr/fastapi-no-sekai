import os
from logging.config import dictConfig
from typing import Any

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

LOGGING_CONFIG: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "app": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}


def setup_logging() -> None:
    """アプリケーション全体のロギング設定を初期化する

    Description:
    - `app.*` 配下のロガーと uvicorn 系ロガーを共通フォーマットに統一する
    - `LOG_LEVEL` 環境変数でレベルを切り替え可能（デフォルト: INFO）
    """
    dictConfig(LOGGING_CONFIG)
