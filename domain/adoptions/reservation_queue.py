from datetime import datetime, timezone

class ReservationQueue:
    """
    Representa uma entrada na fila de reserva de adoção de um animal.
    Modela a intenção de um adotante em reservar um animal,
    incluindo um índice de compatibilidade que pode ser utilizado para
    priorização quando houver múltiplos interessados.

    Attributes:
        animal_id (int): Identificador do animal que está sendo reservado.
        adopter_id (int): Identificador do adotante interessado.
        compatibility_rate (float): Taxa de compatibilidade entre o animal e o adotante (varia de 0 a 100).
        timestamp (datetime | str): Data e hora em que a intenção de reserva foi registrada.
    """

    def __init__(
        self,
        animal_id: int,
        adopter_id: int,
        compatibility_rate: float,
        id = None,
        timestamp: datetime | str = datetime.now(timezone.utc)
    ):
        self.__id = id
        self.animal_id = animal_id
        self.adopter_id = adopter_id
        self.compatibility_rate = compatibility_rate
        self.timestamp = timestamp 

    # -------------------------- PROPERTIES --------------------------

    # ---- ID ----
    @property
    def id(self) -> int:
        return self.__id

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

    # ---- Compatibility Rate ----
    @property
    def compatibility_rate(self) -> float:
        return self.__compatibility_rate
    
    @compatibility_rate.setter
    def compatibility_rate(self, v: float) -> None:
        if not isinstance(v, (int, float)):
            raise TypeError("compatibility_rate deve ser numérico.")
        if not (0 <= v <= 100):
            raise ValueError("compatibility_rate deve estar entre 0 e 100.")
        self.__compatibility_rate = float(v)

    # ---- Timestamp ----
    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, v: datetime | str) -> None:
        if isinstance(v, datetime):
            self.__timestamp = v
            return

        if isinstance(v, str):
            try:
                self.__timestamp = datetime.fromisoformat(v)
                return
            except ValueError:
                raise ValueError(
                    "timestamp inválido. Use datetime ou string ISO 8601 (YYYY-MM-DDTHH:MM:SS)."
                )

        raise TypeError("timestamp deve ser datetime ou string ISO 8601.")