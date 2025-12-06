from domain.animals.animal import Animal
from domain.animals.mixins import VaccinableMixin, TrainableMixin

class Dog(Animal,  VaccinableMixin, TrainableMixin):
    """Cachorro com características específicas."""

    def __init__(self, *args, needs_walk: bool = True, **kwargs):
        Animal.__init__(self, *args, **kwargs)
        VaccinableMixin.__init__(self)
        TrainableMixin.__init__(self)
