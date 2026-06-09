from sqlalchemy.orm import Session

from app.contexts.shared.unit_of_work import UnitOfWork


class SqlAlchemyUnitOfWork(UnitOfWork):
    """SQLAlchemy を用いた Unit of Work の実装クラス

    Description:
    - SQLAlchemy の Session を通じてトランザクションを管理する
    """

    def __init__(self, db: Session):
        self.db = db

    def commit(self) -> None:
        """セッションの変更をコミットする"""
        self.db.commit()

    def rollback(self) -> None:
        """セッションの変更をロールバックする"""
        self.db.rollback()
