from datetime import datetime

class Adoption:
    """Representa o registro de uma adoção.
    Vincula um animal disponível a um adotante elegível,
    registrando a taxa aplicada e o momento da realização da adoção.

    Attributes:
        _id (str): Identificador único da adoção.
        animal (Cat | Dog): Animal adotado.
        adopter (Adopter): Pessoa que realizou a adoção.
        fee (float): Taxa cobrada pela adoção.
        created_at (datetime): Data e hora da adoção.
    """
    def __init__(
        self, id: int,
        animal_id: int,
        adopter_id: int,
        fee: float,
        created_at
        ):
        self.__id = id
        self.animal_id = animal_id
        self.adopter_id = adopter_id
        self.fee = fee
        self.__created_at = created_at

    # -------------------------- PROPERTIES --------------------------

    # ---- ID ----
    @property
    def id(self) -> str:
        return self.__id
    
    # ---- Fee ----
    @property
    def fee(self) -> float:
        return self.__fee

    @fee.setter
    def fee(self, v: float) -> None:
        if v < 0:
            raise ValueError("fee não pode ser negativa.")
        self.__fee = v

    # ---- Date ----
    @property
    def created_at(self) -> datetime:
        return self.__created_at
    
    @created_at.setter
    def created_at(self, v) -> None:
        if not isinstance(v, datetime):
            raise TypeError("created_at deve ser do tipo datetime.")
        self.__created_at = v