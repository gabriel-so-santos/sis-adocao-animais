from abc import ABC, abstractmethod
from datetime import datetime
from domain.enums.animal_status import AnimalStatus
from domain.enums.animal_enums import *
from domain.exceptions import InvalidStatusTransitionError

class Animal(ABC):
    """
    Classe abstrata que representa um animal registrado no sistema.

    Attributes:
        id (str): Identificador único do animal.
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
        species: Species,
        breed: str,
        name: str,
        gender: Gender,
        age_months: int,
        size: Size,
        temperament: list[str],
        status: AnimalStatus,
        id: int = None,
        timestamp: datetime = datetime.now()
    ):
        self.species = species
        self.breed = breed
        self.name = name
        self.gender = gender
        self.age_months = age_months
        self.size = size
        self.temperament = temperament or []
        self.status = status
        self._id = id
        self._timestamp = timestamp


    def __str__(self):
        return f"{self.name}, {self.species_format()} {self.breed}"
    
    # -------------------------- PROPERTIES --------------------------

    # ---- ID ----
    @property
    def id(self) -> str:
        return self._id
    
    # ---- Timestamp ----
    @property
    def timestamp(self) -> datetime:
        return self._timestamp

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
        if not isinstance(v, str):
            raise TypeError("breed deve ser uma string não vazia.")
        if not v.strip():
            raise ValueError("breed deve ser uma string não vazia.")
        self._breed = v.strip().capitalize()

    # ---- Name ----
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, v: str) -> None:
        if not isinstance(v, str):
            raise TypeError("name deve ser uma string não vazia.")
        if not v.strip():
            raise ValueError("name deve ser uma string não vazia.")
        self._name = v.strip().capitalize()

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
        
        self._temperament = [item.strip().capitalize() for item in v if item.strip()]

    # ---- Status ----
    @property
    def status(self) -> AnimalStatus:
        return self._status

    @status.setter
    def status(self, v: AnimalStatus) -> None:
        if not isinstance(v, AnimalStatus):
            raise TypeError("status deve ser um item do enum AnimalStatus.")
        
        current = getattr(self, "_status", None)

        if current is not None:
            if not AnimalStatus.is_valid_transition(current, v):
                raise InvalidStatusTransitionError(f"Transição inválida! {current} -> {v}")

        self._status = v

    # -------------------------- FORMAT METHODS --------------------------

    @abstractmethod
    def extra_info(self):
        pass

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
        return ", ".join(item for item in self.temperament)
    
    def status_format(self):
        return {
            "AVAILABLE": "Disponível",
            "RESERVED": "Reservado",
            "ADOPTED": "Adotado",
            "RETURNED": "Devolvido",
            "QUARANTINE": "Em Quarentena",
            "UNADOPTABLE": "Indisponível"
        }.get(self.status.name)