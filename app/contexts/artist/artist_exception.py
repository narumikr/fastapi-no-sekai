from enum import Enum

from app.contexts.shared.exceptions import BussinessException, ErrorDetails


class ArtistError(Enum):
    """アーティストドメインのエラーコードとメッセージ定義

    エラーはこのクラスで一元管理する
    """

    NAME_REQUIRED = "アーティスト名は必須です。"

    DUPLICATE_NAME = "同じアーティスト名が既に存在しています。"


class ArtistBadRequestException(BussinessException):
    """アーティストドメインのビジネス例外クラス

    Status Code: 400 Bad Request
    """

    def __init__(self, error: ArtistError, details: list[ErrorDetails] | None = None):
        super().__init__(code=error.name, message=error.value, details=details)


class ArtistDuplicateNameException(BussinessException):
    """アーティストドメインの重複エラークラス

    Status Code: 409 Conflict
    """

    def __init__(self, error: ArtistError, details: list[ErrorDetails] | None = None):
        super().__init__(code=error.name, message=error.value, details=details)
