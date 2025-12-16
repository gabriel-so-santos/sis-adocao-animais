from datetime import datetime
from domain.animals.animal import Animal, Species, Gender, Size, AnimalStatus
from domain.mixins.vaccinable_mixin import  VaccinableMixin
from typing import override

class Cat(VaccinableMixin, Animal):
    """Gato com características específicas."""
    html_icon = "fa-solid fa-cat"

    def __init__(self,
        species: Species,
        breed: str,
        name: str,
        gender: Gender,
        age_months: int,
        size: Size,
        temperament: list[str],
        status: AnimalStatus,
        is_hypoallergenic: bool,
        id: int = None,
        timestamp: datetime = datetime.now()
        ):

        super().__init__(
            species, breed, name, gender, age_months, size, temperament, status, id, timestamp
        )

        self.is_hypoallergenic = is_hypoallergenic
    
    # -------------------------- PROPERTIES --------------------------

    # ---- is_hypoallergenic ----
    @property
    def is_hypoallergenic(self) -> bool:
        return self.__is_hypoallergenic
    
    @is_hypoallergenic.setter
    def is_hypoallergenic(self, v: bool) -> None:
        if not isinstance(v, bool):
            raise TypeError("is_hypoallergenic deve ser um booleano.")
        self.__is_hypoallergenic = v

    # -------------------------- FORMAT METHODS --------------------------
    
    @override
    def extra_info(self):
        return f"<strong>É Hipoalergênico?:</strong> {'Sim' if self.is_hypoallergenic else 'Não'}"
    
    def is_hypoallergenic_format(self):
        return 'Sim' if self.is_hypoallergenic else 'Não'