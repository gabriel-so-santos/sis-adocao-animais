from abc import ABC
from uuid import uuid
from animal_status import *

class Gender(Enum):
    MALE = auto()
    FEMALE = auto()

class Size(Enum):
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()

class Animal(ABC):
    """Classe abstrata que representa um animal registrado no sistema.

    Attributes:
        _id (str): Identificador único do animal.
        species (str): Espécie do animal (ex.: "Gato", "Cachorro").
        breed (str): Raça do animal.
        name (str): Nome do animal.
        gender (Gender): Gênero do animal.
        age_months (int): Idade do animal em meses.
        size (Size): Porte do animal (pequeno, médio, grande).
        temperament (list) Temperamento do animal.
        status (AnimalStatus): Estado atual do animal no sistema.
    """
    def __init__(
        self,
        species: str,
        breed: str,
        name: str,
        gender: Gender,
        age_months: int,
        size: Size,
        temperament: list,
        status: AnimalStatus = AnimalStatus.AVAILABLE,
    ):
        self._id = uuid.uuid4().hex
        self.species = species
        self.breed = breed
        self.name = name
        self.gender = gender
        self.age_months = age_months
        self.size = size
        self.temperament = temperament or []
        self.status = status

    @property
    def id(self) -> str:
        return self._id

    @property
    def age_months(self) -> int:
        return self._age_months

    @age_months.setter
    def set_age_months(self, v: int) -> None:
        self._age_months = v

    @property
    def size(self) -> Size:
        return self._size

    @size.setter
    def set_size(self, v: Size) -> None:
        self._size = v