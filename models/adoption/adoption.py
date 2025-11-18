from uuid import uuid
from datetime import datetime
from animals import Cat, Dog
from people import Adopter


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
    def __init__(self, animal: Cat|Dog, adopter: Adopter, fee: float) -> None:
        self._id = uuid.uuid4().hex
        self.animal = animal
        self.adopter = adopter
        self.fee = fee
        self.adoption_date = datetime.now

    @property
    def id(self) -> str:
        return self._id