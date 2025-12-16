from datetime import datetime, timezone, timedelta
import json

with open("settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)

duration_hours = settings["policies"]["reservation_duration_hours"]

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
        is_canceled: bool = False,
        id = None,
        timestamp: datetime = datetime.now()
    ):
        self.animal_id = animal_id
        self.adopter_id = adopter_id
        self.compatibility_rate = compatibility_rate
        self.is_canceled = is_canceled
        self.__id = id
        self.__timestamp = timestamp 

    def __lt__(self, rq: "ReservationQueue") -> bool:
        if self.compatibility_rate != rq.compatibility_rate:
            return self.compatibility_rate > rq.compatibility_rate
        
        return self.timestamp < rq.timestamp
    
    def check_expiration(self) -> bool:
        """
        Verifica se a reserva expirou com base na duração configurada.

        Args:
            duration_hours (int): Duração máxima da reserva em horas.

        Returns:
            bool: True se a reserva expirou, False caso contrário.
        """
        expiration_time = self.timestamp + timedelta(hours=duration_hours)

        if datetime.now(timezone.utc) >= expiration_time:
            self.has_ended = True
            return True

        return False

    # -------------------------- PROPERTIES --------------------------

    # ---- Timestamp ----
    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

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

    # ---- Is Canceled ----
    @property
    def is_canceled(self) -> bool: 
        return self.__is_canceled
    
    @is_canceled.setter
    def is_canceled(self, v: bool) -> None:
        if not isinstance(v, bool):
            raise TypeError("is_canceled deve ser um booleano.")
        self.__is_canceled = v