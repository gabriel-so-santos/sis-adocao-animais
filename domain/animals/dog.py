from domain.animals.animal import Animal
from domain.animals.mixins import VaccinableMixin, TrainableMixin

class Dog(Animal,  VaccinableMixin, TrainableMixin):
    """Cachorro com características específicas."""
    html_icon = "fa-solid fa-dog"

    def __init__(self, *args, needs_walk: bool, **kwargs):
        Animal.__init__(self, *args, **kwargs)
        VaccinableMixin.__init__(self)
        TrainableMixin.__init__(self)
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
