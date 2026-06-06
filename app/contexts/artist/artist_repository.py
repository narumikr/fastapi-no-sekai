from abc import ABC, abstractmethod

from app.contexts.artist.artist_models import Artist


class ArtistRepository(ABC):
    """アーティストに関するリポジトリインターフェース"""

    @abstractmethod
    def save_artist(self, artist: Artist) -> Artist:
        """アーティストを永続化する

        Args:
        - artist: Artist - 作成するアーティストの情報

        Returns:
        - Artist: 永続化されたアーティストの情報
        """
        pass
