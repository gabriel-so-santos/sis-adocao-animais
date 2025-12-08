from domain.animals.animal import Animal, Species, Gender, Size, AnimalStatus
from domain.mixins.vaccinable_mixin import  VaccinableMixin
from domain.mixins.trainable_mixin import TrainableMixin

class Dog(VaccinableMixin, TrainableMixin, Animal):
    """Cachorro com características específicas."""
    html_icon = "fa-solid fa-dog"

    def __init__(self,
        id: int,
        species: Species,
        breed: str,
        name: str,
        gender: Gender,
        age_months: int,
        size: Size,
        temperament: list[str] | None,
        status: AnimalStatus,

        needs_walk: bool
        ):

        super().__init__(
            id, species, breed, name, gender, age_months, size, temperament, status
        )
        self.needs_walk = needs_walk

    def extra_info(self):
        return f"Precisa de passeio?: {'Sim' if self.needs_walk else 'Não'}"

    @property
    def needs_walk(self) -> bool:
        return self.__needs_walk
    
    @needs_walk.setter
    def needs_walk(self, v: bool) -> None:
        if not isinstance(v, bool):
            raise TypeError("needs_walk deve ser um booleano.")
        self.__needs_walk = v
