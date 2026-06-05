from app.contexts.artist.artist_exception import ArtistBadRequestException, ArtistError


class Artist:
    """アーティストドメインモデル

    アーティストのマスタデータを永続化するためのドメインモデル
    """

    def __init__(
        self,
        id: int | None,
        artist_name: str,
        unit_name: str | None,
    ):
        if not artist_name:
            raise ArtistBadRequestException(ArtistError.NAME_REQUIRED)

        self.id = id
        self.artist_name = artist_name
        self.unit_name = unit_name

    """新規アーティスト作成
    
    Args:
    - artist_name: アーティスト名
    - unit_name: ユニット名（任意）
    """

    @classmethod
    def create_new_artist(
        cls, artist_name: str, unit_name: str | None = None
    ) -> Artist:
        return cls(id=None, artist_name=artist_name, unit_name=unit_name)

    """既存アーティストの更新

    Args:
    - artist_name: アーティスト名（任意）
    - unit_name: ユニット名（任意）
    """

    def update_artist(self, artist_name: str | None, unit_name: str | None) -> Artist:
        return Artist(
            id=self.id,
            artist_name=artist_name if artist_name is not None else self.artist_name,
            unit_name=unit_name if unit_name is not None else self.unit_name,
        )
