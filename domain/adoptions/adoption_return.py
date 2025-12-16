from datetime import datetime, timezone

class AdoptionReturn:
    """Representa o registro da devolução de um animal adotado.
    Armazena o motivo e a data da devolução, mantendo vínculo com a adoção
    original para controle histórico.

    Attributes:
        id (int): Identificador único da devolução.
        adoption_id (int): ID da adoção à qual a devolução está associada.
        reason (str): Motivo informado para a devolução.
        timestamp (datetime | str): Data e hora em que a devolução foi registrada.
    """

    def __init__(
        self,
        adoption_id: int,
        reason: str,
        timestamp: datetime = datetime.now()
    ):
        self.adoption_id = adoption_id
        self.reason = reason
        self.__timestamp = timestamp

    # -------------------------- PROPERTIES --------------------------

    # ---- ID ----
    @property
    def adoption_id(self) -> int:
        return self.__id

     # ---- Timestamp ----
    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    # ---- Adoption ID ----
    @property
    def adoption_id(self) -> int:
        return self.__adoption_id

    @adoption_id.setter
    def adoption_id(self, v: int) -> None:
        if not isinstance(v, int):
            raise TypeError("adoption_id deve ser do tipo int.")
        self.__adoption_id = v

    # ---- Reason ----
    @property
    def reason(self) -> str:
        return self.__reason

    @reason.setter
    def reason(self, v: str) -> None:
        if not isinstance(v, str):
            raise TypeError("reason deve ser do tipo str.")
        self.__reason = v