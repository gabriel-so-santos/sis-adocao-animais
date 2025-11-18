from animal import Animal
from mixins import VaccinableMixin, TrainableMixin

class Dog(Animal,  VaccinableMixin, TrainableMixin):
    """Cachorro com características específicas."""

    def __init__(self, *args, needs_walk: bool = True, **kwargs) -> None:
        Animal.__init__(self, *args, **kwargs)
        VaccinableMixin.__init__(self)
        TrainableMixin.__init__(self)
