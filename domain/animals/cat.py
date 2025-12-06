from domain.animals.animal import Animal
from domain.animals.mixins import VaccinableMixin

class Cat(Animal, VaccinableMixin):
    """Gato com características específicas."""

    def __init__(self, *args, independence: bool = True, **kwargs):
        Animal.__init__(self, *args, **kwargs)
        VaccinableMixin.__init__(self)