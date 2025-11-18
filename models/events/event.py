from datetime import datetime

class Event:
    """Representa um evento associado a um animal.
    Exemplos de eventos incluem: entrada no sistema, aplicação de vacina,
    mudança de status, adoção e devolução.

    Attributes:
        timestamp (datetime): Instante em que o evento ocorreu.
        event_type (str): Tipo do evento.
        description (str): Descrição do evento.
    """
    def __init__(self, event_type: str, description: str):
        self.timestamp: datetime = datetime.now()
        self.event_type = event_type
        self.description = description