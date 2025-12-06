from abc import ABC
from enum import Enum
from domain.animals.animal_status import AnimalStatus

class Species(Enum):
    CAT = "CAT"
    DOG = "DOG"

class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"

class Size(Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"

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
        temperament (list[str]): Lista de características temperamentais.
        status (AnimalStatus): Estado atual do animal no sistema.
    """
    def __init__(
        self,
        id: int,
        species: Species,
        breed: str,
        name: str,
        gender: Gender,
        age_months: int,
        size: Size,
        temperament: list[str] | None,
        status: AnimalStatus = AnimalStatus.AVAILABLE,
    ):
        self._id = id
        self.species = species
        self.breed = breed.capitalize()
        self.name = name.capitalize()
        self.gender = gender
        self.age_months = age_months
        self.size = size
        self.temperament = temperament or []
        self.status = status

    def species_format(self):
        if self.gender == Gender.FEMALE:
            return {
                "CAT": "Gata",
                "DOG": "Cadela",
            }.get(self.species.name)
        
        else:
            return {
                "CAT": "Gato",
                "DOG": "Cachorro",
            }.get(self.species.name)
    
    def gender_format(self):
        return {
            "MALE": "Macho",
            "FEMALE": "Fêmea",
        }.get(self.gender.name)
    
    def size_format(self):
        return {
            "SMALL": "Pequeno",
            "MEDIUM": "Médio",
            "LARGE": "Grande"
        }.get(self.size.name)
    
    def temperament_format(self):
        return ", ".join(item.strip().capitalize() for item in self.temperament)
    
    def status_format(self):
        return {
            "AVAILABLE": "Disponível",
            "RESERVED": "Reservado",
            "ADOPTED": "Adotado",
            "RETURNED": "Devolvido",
            "QUARANTINE": "Em Quarentena",
            "UNADOPTABLE": "Indisponível"
        }.get(self.status.name)
    
    # -------------------------- PROPERTIES --------------------------

    # ---- ID ----
    @property
    def id(self) -> str:
        return self._id

    # ---- Species ----
    @property
    def species(self) -> Species:
        return self._species

    @species.setter
    def species(self, v: str) -> None:
        if not isinstance(v, Species):
            raise ValueError("species deve ser do tipo Species.")
        self._species = v

    # ---- Breed ----
    @property
    def breed(self) -> str:
        return self._breed

    @breed.setter
    def breed(self, v: str) -> None:
        if not v.strip() or not isinstance(v, str):
            raise ValueError("breed deve ser uma string não vazia.")
        self._breed = v

    # ---- Name ----
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, v: str) -> None:
        if not v.strip() or not isinstance(v, str):
            raise ValueError("name deve ser uma string não vazia.")
        self._name = v

    # ---- Gender ----
    @property
    def gender(self) -> Gender:
        return self._gender

    @gender.setter
    def gender(self, v: Gender) -> None:
        if not isinstance(v, Gender):
            raise TypeError("gender deve ser um item do enum Gender.")
        self._gender = v

    # ---- Age (months) ----
    @property
    def age_months(self) -> int:
        return self._age_months

    @age_months.setter
    def age_months(self, v: int) -> None:
        if not isinstance(v, int):
            raise TypeError("age_months deve ser int.")
        if v < 0:
            raise ValueError("age_months não pode ser negativo.")
        self._age_months = v

    # ---- Size ----
    @property
    def size(self) -> Size:
        return self._size

    @size.setter
    def size(self, v: Size) -> None:
        if not isinstance(v, Size):
            raise TypeError("size deve ser um item do enum Size.")
        self._size = v

    # ---- Temperament ----
    @property
    def temperament(self) -> list[str]:
        return self._temperament

    @temperament.setter
    def temperament(self, v: list[str]) -> None:
        if not isinstance(v, list):
            raise TypeError("temperament deve ser uma lista.")
        if not all(isinstance(item, str) for item in v):
            raise TypeError("temperament deve conter apenas strings.")
        self._temperament = v

    # ---- Status ----
    @property
    def status(self) -> AnimalStatus:
        return self._status

    @status.setter
    def status(self, v: AnimalStatus) -> None:
        if not isinstance(v, AnimalStatus):
            raise TypeError("status deve ser um item do enum AnimalStatus.")
        self._status = v