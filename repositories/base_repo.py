from abc import ABC, abstractmethod
from typing import Any

class BaseRepository(ABC):
    """Interface base para repositórios."""

    @abstractmethod
    def save(self, obj: Any) -> Any:
        pass

    @abstractmethod
    def update(self, obj: Any) -> Any:
        pass

    @abstractmethod
    def delete(self, obj_id: str) -> None:
        pass

    @abstractmethod
    def get_by_id(self, obj_id: str) -> Any:
        pass