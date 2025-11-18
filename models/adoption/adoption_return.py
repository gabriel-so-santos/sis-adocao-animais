from uuid import uuid
from datetime import datetime
from adoption import Adoption

class AdoptionReturn:
    """Representa o registro da devolução de um animal adotado.
    Armazena o motivo e a data da devolução, mantendo vínculo com a adoção
    original para controle histórico.

    Attributes:
        _id (str): Identificador único da devolução.
        adoption (Adoption): Adoção à qual a devolução está associada.
        reason (str): Motivo informado para a devolução.
        date (datetime): Data e hora em que a devolução foi registrada.
    """

    def __init__(self, adoption: Adoption, reason: str) -> None:
        self._id = uuid.uuid4().hex
        self.adoption = adoption
        self.reason = reason
        self.date = datetime.now
