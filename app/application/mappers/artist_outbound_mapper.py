from app.application.dtos.artist_dtos import ArtistDto


class ArtistOutboundMapper:
    """ドメインモデルから内部DTOへの変換などアウトバウンドマッピングを行うクラス"""

    @staticmethod
    def to_artist_dto(artist) -> ArtistDto:
        """ドメインモデルをアーティストの内部DTOに変換"""
        return ArtistDto(
            id=artist.id,
            artist_name=artist.artist_name,
            unit_name=artist.unit_name,
            meta_info=artist.meta_info,
        )
