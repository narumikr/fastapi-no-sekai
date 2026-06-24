import pytest

from app.contexts.artist.artist_exception import ArtistBadRequestException
from app.contexts.artist.artist_models import Artist


class TestArtistCreate:
    def test_名前とユニット名を指定して新規アーティストを作成できる(self):
        artist = Artist.create_new_artist(artist_name="Leo/need", unit_name="Leo/need")

        assert artist.id is None
        assert artist.artist_name == "Leo/need"
        assert artist.unit_name == "Leo/need"
        assert artist.meta_info is None

    def test_ユニット名を省略して新規アーティストを作成できる(self):
        artist = Artist.create_new_artist(artist_name="MEIKO")

        assert artist.unit_name is None

    def test_アーティスト名が空文字のとき作成に失敗する(self):
        with pytest.raises(ArtistBadRequestException):
            Artist.create_new_artist(artist_name="")

    def test_アーティスト名がスペースのみのとき作成に失敗する(self):
        with pytest.raises(ArtistBadRequestException):
            Artist.create_new_artist(artist_name="   ")


class TestArtistUpdate:
    def test_アーティスト名を更新できる(self):
        artist = Artist.create_new_artist(artist_name="Leo/need")

        updated = artist.update_artist(artist_name="KAITO", unit_name=None)

        assert updated.artist_name == "KAITO"

    def test_アーティスト名にNoneを渡すと既存の名前が維持される(self):
        artist = Artist.create_new_artist(artist_name="Leo/need")

        updated = artist.update_artist(artist_name=None, unit_name=None)

        assert updated.artist_name == "Leo/need"

    def test_アーティスト名が空文字のとき更新に失敗する(self):
        artist = Artist.create_new_artist(artist_name="Leo/need")

        with pytest.raises(ArtistBadRequestException):
            artist.update_artist(artist_name="", unit_name=None)

    def test_ユニット名を更新できる(self):
        artist = Artist.create_new_artist(artist_name="Leo/need", unit_name="OLD_UNIT")

        updated = artist.update_artist(artist_name=None, unit_name="NEW_UNIT")

        assert updated.unit_name == "NEW_UNIT"

    def test_ユニット名にNoneを渡すと既存のユニット名が維持される(self):
        artist = Artist.create_new_artist(artist_name="Leo/need", unit_name="Leo/need")

        updated = artist.update_artist(artist_name=None, unit_name=None)

        assert updated.unit_name == "Leo/need"
