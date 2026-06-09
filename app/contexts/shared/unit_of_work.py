from abc import ABC, abstractmethod


class UnitOfWork(ABC):
    """Unit of Work インターフェース

    Description:
    - トランザクションの境界を管理するための抽象クラス
    - 永続化操作をまとめてコミットまたはロールバックする責務を持つ
    """

    @abstractmethod
    def commit(self) -> None:
        """変更をコミットする"""
        pass

    @abstractmethod
    def rollback(self) -> None:
        """変更をロールバックする"""
        pass
