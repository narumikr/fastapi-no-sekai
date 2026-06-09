from fastapi import Depends
from sqlalchemy.orm import Session

from app.adapter.infrastructure.artist_repository_impl import ArtistRepositoryImpl
from app.adapter.infrastructure.sqlalchemy_unit_of_work import SqlAlchemyUnitOfWork
from app.application.usecases.artist_usecase import ArtistUseCase
from app.core.database import get_db


def get_artist_usecase(db: Session = Depends(get_db)) -> ArtistUseCase:
    """ArtistUseCase の DI ファクトリ関数

    Description:
    - DB セッションから Unit of Work とリポジトリを生成し、ArtistUseCase を返す
    - Controller はこの関数を通じてユースケースを受け取り、
      DB やリポジトリの詳細を知る必要がない
    """
    unit_of_work = SqlAlchemyUnitOfWork(db=db)
    repository = ArtistRepositoryImpl(db=db)
    return ArtistUseCase(artist_repository=repository, unit_of_work=unit_of_work)
