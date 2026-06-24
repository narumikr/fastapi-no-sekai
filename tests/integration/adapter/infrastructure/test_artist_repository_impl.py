import pytest
from sqlalchemy.orm import Session

from app.adapter.infrastructure.artist_repository_impl import ArtistRepositoryImpl
from app.contexts.artist.artist_exception import ArtistDuplicateNameException
from app.contexts.artist.artist_models import Artist


class TestSaveArtist:
    def test_新規アーティストを永続化するとIDとメタ情報が付与される(
        self, db_session: Session
    ):
        repo = ArtistRepositoryImpl(db=db_session)
        artist = Artist.create_new_artist(artist_name="Leo/need", unit_name="Leo/need")

        saved = repo.save_artist(artist)
        db_session.commit()

        assert saved.id is not None
        assert saved.artist_name == "Leo/need"
        assert saved.unit_name == "Leo/need"
        assert saved.meta_info is not None
        assert saved.meta_info.created_at is not None
        assert saved.meta_info.version == 1

    def test_アーティスト名が重複のとき例外が発生する(self, db_session: Session):
        repo = ArtistRepositoryImpl(db=db_session)
        artist1 = Artist.create_new_artist(artist_name="Leo/need")
        repo.save_artist(artist1)
        db_session.commit()

        artist2 = Artist.create_new_artist(artist_name="Leo/need")
        with pytest.raises(ArtistDuplicateNameException):
            repo.save_artist(artist2)
