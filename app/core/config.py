import os
from zoneinfo import ZoneInfo

# 環境変数からタイムゾーン名を取得（デフォルト: UTC）
TIMEZONE_NAME = os.getenv("APP_TIMEZONE", "UTC")


def get_timezone():
    """設定されたタイムゾーン名から tzinfo を返します。

    ZoneInfo を使用して IANA タイムゾーン名（例: 'Asia/Tokyo' や 'UTC'）を扱います。
    エラーが発生した場合は 'UTC' を返します。
    """
    try:
        return ZoneInfo(TIMEZONE_NAME)
    except Exception:
        return ZoneInfo("UTC")
