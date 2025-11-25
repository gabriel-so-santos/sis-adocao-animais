import uuid
from datetime import datetime
from models.animals.cat import Cat
from models.animals.dog import Dog
from models.people.adopter import Adopter

class Adoption:
    """Representa o registro de uma adoção.
    Vincula um animal disponível a um adotante elegível,
    registrando a taxa aplicada e o momento da realização da adoção.

    Attributes:
        _id (str): Identificador único da adoção.
        animal (Cat | Dog): Animal adotado.
        adopter (Adopter): Pessoa que realizou a adoção.
        fee (float): Taxa cobrada pela adoção.
        adoption_date (datetime): Data e hora da adoção.
    """
    def __init__(self, animal: Cat | Dog, adopter: Adopter, fee: float):
        self._id = uuid.uuid4().hex
        self.animal = animal
        self.adopter = adopter
        self.fee = fee
        self._adoption_date = datetime.now()

    # -------------------------- PROPERTIES --------------------------

    # ---- ID ----
    @property
    def id(self) -> str:
        return self._id

    # ---- Animal ----
    @property
    def animal(self) -> Cat | Dog:
        return self._animal

    @animal.setter
    def animal(self, v: Cat | Dog) -> None:
        if not isinstance(v, (Cat, Dog)):
            raise TypeError("animal deve ser instância de Cat ou Dog.")
        self._animal = v

    # ---- Adopter ----
    @property
    def adopter(self) -> Adopter:
        return self._adopter

    @adopter.setter
    def adopter(self, v: Adopter) -> None:
        if not isinstance(v, Adopter):
            raise TypeError("adopter deve ser instância de Adopter.")
        self._adopter = v

    # ---- Fee ----
    @property
    def fee(self) -> float:
        return self._fee

    @fee.setter
    def fee(self, v: float) -> None:
        if v < 0:
            raise ValueError("fee não pode ser negativa.")
        self._fee = v

    # ---- Date ----
    @property
    def adoption_date(self) -> datetime:
        return self._adoption_date