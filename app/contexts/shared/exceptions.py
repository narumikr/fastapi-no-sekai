from dataclasses import dataclass


@dataclass
class ErrorDetails:
    """エラーの詳細情報を表すクラス

    エラーの詳細情報はフィールド名とメッセージを含むことができる
    """

    message: str  # エラーの説明
    field: str | None = None  # エラーが発生したフィールド名


class BussinessException(Exception):
    """ドメイン層の例外を表す基底クラス

    ドメイン層の例外はすべてこのクラスを継承して定義する
    """

    def __init__(
        self, code: str, message: str, details: list[ErrorDetails] | None = None
    ):
        self.code = code  # エラーの識別子
        self.message = message  # エラーの説明
        self.details = details if details is not None else []  # エラーの詳細情報
        super().__init__(message)
