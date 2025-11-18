from typing import Any
from base_repo import BaseRepository

class SqliteRepository(BaseRepository):
    """Esqueleto de repositório para SQLite."""

    def save(self, obj: Any) -> Any:
        pass

    def update(self, obj: Any) -> Any:
        pass

    def delete(self, obj_id: str) -> None:
        pass

    def get_by_id(self, obj_id: str) -> Any:
        pass