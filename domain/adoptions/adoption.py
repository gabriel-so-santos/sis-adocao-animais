from datetime import datetime, timezone

class Adoption:
    """
    Representa o registro de uma adoção.
    Vincula um animal disponível a um adotante elegível,
    registrando a taxa aplicada e o momento da realização da adoção.

    Attributes:
        id (int): Identificador único da adoção.
        animal_id (int): ID do animal adotado.
        adopter_id (int): ID da pessoa que realizou a adoção.
        fee (float): Taxa cobrada pela adoção.
        timestamp (datetime | str): Data e hora da adoção.
    """
    def __init__(
        self,
        animal_id: int,
        adopter_id: int,
        fee: float,
        id: int = None,
        timestamp: datetime = datetime.now()
    ):
        self.animal_id = animal_id
        self.adopter_id = adopter_id
        self.fee = fee
        self.__id = id
        self.__timestamp = timestamp

    # -------------------------- PROPERTIES --------------------------

    # ---- ID ----
    @property
    def id(self) -> int:
        return self.__id
    
    # ---- Timestamp ----
    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    # ---- Animal ID ----
    @property
    def animal_id(self) -> int:
        return self.__animal_id
    
    @animal_id.setter
    def animal_id(self, v: int) -> None:
        if not isinstance(v, int):
            raise TypeError("animal_id deve ser do tipo int.")
        if v < 1:
            raise ValueError("animal_id deve ser maior que 0.")
        self.__animal_id = v

    # ---- Adopter ID ----
    @property
    def adopter_id(self) -> int:
        return self.__adopter_id
    
    @adopter_id.setter
    def adopter_id(self, v: int) -> None:
        if not isinstance(v, int):
            raise TypeError("adopter_id deve ser do tipo int.")
        if v < 1:
            raise ValueError("adopter_id deve ser maior que 0.")
        self.__adopter_id = v

    # ---- Fee ----
    @property
    def fee(self) -> float:
        return self.__fee

    @fee.setter
    def fee(self, v: float) -> None:
        if not isinstance(v, (int, float)):
            raise TypeError("fee deve ser numérico.")
        if v < 0:
            raise ValueError("fee não pode ser negativa.")
        self.__fee = float(v)