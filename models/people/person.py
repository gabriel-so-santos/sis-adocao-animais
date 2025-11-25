from abc import ABC
from _uuid import uuid

class Person(ABC):
    """Classe base abstrata para representar pessoas do sistema.

    Attributes:
        _id (str): Identificador único da pessoa.
        name (str): Nome da pessoa.
        age (int): Idade da pessoa.
    """

    def __init__(self, name: str, age: int) -> None:
        self._id = uuid.uuid4().hex
        self.name = name
        self.age = age

    # -------------------------- PROPERTIES --------------------------

    # ---- ID ----
    @property
    def id(self) -> str:
        return self._id

    # ---- Name ----
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, v: str) -> None:
        if not v.strip() or not isinstance(v, str):
            raise ValueError("name deve ser uma string não vazia.")
        self._name = v

    # ---- Age ----
    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, v: int) -> None:

        if not isinstance(v, int):
            raise TypeError("age deve ser do tipo int.")
        
        if not (0 < v < 120):
            raise ValueError("Idade fora do intervalo permitido.")
        
        self._age = v