from app.contexts.artist.artist_exception import ArtistBadRequestException, ArtistError
from app.contexts.shared.meta_models import MetaModel


class Artist:
    """アーティストドメインモデル

    アーティストのマスタデータを永続化するためのドメインモデル
    """

    def __init__(
        self,
        id: int | None,
        artist_name: str,
        unit_name: str | None,
        meta_info: MetaModel | None = None,
    ):
        self._validate_artist_name(artist_name)

        self.id = id
        self.artist_name = artist_name
        self.unit_name = unit_name
        self.meta_info = meta_info

    """新規アーティスト作成
    
    Args:
    - artist_name: アーティスト名
    - unit_name: ユニット名（任意）
    """

    @classmethod
    def create_new_artist(
        cls, artist_name: str, unit_name: str | None = None
    ) -> Artist:
        return cls(
            id=None, artist_name=artist_name, unit_name=unit_name, meta_info=None
        )

    """既存アーティストの更新

    Args:
    - artist_name: アーティスト名（任意）
    - unit_name: ユニット名（任意）
    """

    def update_artist(
        self,
        artist_name: str | None,
        unit_name: str | None,
        meta_info: MetaModel | None = None,
    ) -> Artist:
        if artist_name is not None:
            self._validate_artist_name(artist_name)
            self.artist_name = artist_name

        if unit_name is not None:
            self.unit_name = unit_name

        if meta_info is not None:
            self.meta_info = meta_info

        return self

    """アーティスト名のバリデーションヘルパー
    
    Description:
    - アーティスト名がNoneもしくは空文字、スペースのみ場合はエラーとする
    """

    @staticmethod
    def _validate_artist_name(artist_name: str) -> None:
        if not artist_name or artist_name.strip() == "":
            raise ArtistBadRequestException(ArtistError.NAME_REQUIRED)
