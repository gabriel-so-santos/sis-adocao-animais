from datetime import datetime
from domain.animals.animal import Animal, Species, Gender, Size, AnimalStatus
from domain.mixins.vaccinable_mixin import  VaccinableMixin
from domain.mixins.trainable_mixin import TrainableMixin

from typing import override

class Dog(VaccinableMixin, TrainableMixin, Animal):
    """Cachorro com características específicas."""
    html_icon = "fa-solid fa-dog"

    def __init__(self,
        species: Species,
        breed: str,
        name: str,
        gender: Gender,
        age_months: int,
        size: Size,
        temperament: list[str],
        status: AnimalStatus,
        needs_walk: bool,
        id: int = None,
        timestamp: datetime = datetime.now()
        ):

        super().__init__(
            species, breed, name, gender, age_months, size, temperament, status, id, timestamp
        )
        self.needs_walk = needs_walk

    # -------------------------- PROPERTIES --------------------------

    # ---- needs_walk ----
    @property
    def needs_walk(self) -> bool:
        return self.__needs_walk
    
    @needs_walk.setter
    def needs_walk(self, v: bool) -> None:
        if not isinstance(v, bool):
            raise TypeError("needs_walk deve ser um booleano.")
        self.__needs_walk = v

    # -------------------------- FORMAT METHODS --------------------------

    @override
    def extra_info(self):
        return f"<strong>Precisa de passeio?:</strong> {'Sim' if self.needs_walk else 'Não'}"
    
    def extra_info_str(self):
        return f"Precisa de passeio?: {'Sim' if self.needs_walk else 'Não'}"
    
    def needs_walk_format(self):
        return 'Sim' if self.needs_walk else 'Não'