from domain.animals.animal import Animal
from domain.animals.mixins import VaccinableMixin

class Cat(Animal, VaccinableMixin):
    """Gato com características específicas."""
    html_icon = "fa-solid fa-cat"

    def __init__(self, *args, is_hypoallergenic: bool, **kwargs):
        Animal.__init__(self, *args, **kwargs)
        VaccinableMixin.__init__(self)
        self.is_hypoallergenic = is_hypoallergenic

    def extra_info(self):
        return f"É Hipoalergênico?: {'Sim' if self.is_hypoallergenic else 'Não'}"

    @property
    def is_hypoallergenic(self) -> bool:
        return self.__is_hypoallergenic
    
    @is_hypoallergenic.setter
    def is_hypoallergenic(self, v: bool) -> None:
        if not isinstance(v, bool):
            raise TypeError("is_hypoallergenic deve ser um booleano.")
        self.__is_hypoallergenic = v