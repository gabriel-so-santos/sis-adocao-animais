from abc import ABC
from datetime import datetime, timezone

class Person(ABC):
    """Classe base abstrata para representar pessoas do sistema.

    Attributes:
        id (str): Identificador único da pessoa.
        name (str): Nome da pessoa.
        age (int): Idade da pessoa.
        timestamp (datetime | str): Data e hora do registro da pessoa.
    """

    def __init__(
        self,
        name: str,
        age: int,
        id: int,
        timestamp: datetime
    ):
        self.name = name
        self.age = age
        self._id = id
        self._timestamp = timestamp

    def __str__(self):
        return f"{self.name}, {self.age} anos"

    # -------------------------- PROPERTIES --------------------------

    # ---- ID ----
    @property
    def id(self) -> int:
        return self._id
    
    # ---- Timestamp ----
    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    # ---- Name ----
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, v: str) -> None:
        if not isinstance(v, str):
            raise TypeError("name deve ser do tipo str.")
        if not v.strip():
            raise ValueError("name deve ser uma string não vazia.")
        self._name = v.strip().capitalize()

    # ---- Age ----
    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, v: int) -> None:

        if not isinstance(v, int):
            raise TypeError("age deve ser do tipo int.")
        
        if not (0 <= v <= 128):
            raise ValueError("Idade fora do intervalo permitido.")
        
        self._age = v