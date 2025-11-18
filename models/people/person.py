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

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def set_name(self, v: str) -> None:
        self._name = v

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def set_age(self, v: int) -> None:
        self._age = v

    def validate_age(self) -> bool:
        pass
