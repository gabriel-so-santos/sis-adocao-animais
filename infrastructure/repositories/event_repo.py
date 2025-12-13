from datetime import datetime, timezone
from dataclasses import asdict

from .base_repo import BaseRepository
from typing import override

from infrastructure.db_models.event_model import EventModel
from domain.events.events import Event, EventType

class EventRepository(BaseRepository):
    
    def __init__(self, session):
        super().__init__(session, EventModel)

    @override
    def _to_domain(self, event_model: EventModel) -> Event:
        """
        Converte uma instância de EventModel (SQLAlchemy) em uma entidade de domínio Event,
        reconstruindo os dados conforme o tipo específico do evento.

        Args:
            event_model (EventModel): Instância do modelo persistido no banco,
            contendo os dados do evento registrado.

        Returns:
            Event: Entidade de domínio correspondente ao registro encontrado,
            com os campos convertidos e normalizados.
        """
        from domain.events.event_converter import EventConverter

        timestamp = event_model.timestamp
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)

        event = EventConverter.convert_to_domain_event(
            id=event_model.id,
            animal_id=event_model.animal_id,
            event_type=EventType[event_model.event_type],
            timestamp=timestamp,
            extra_data=event_model.extra_data or {}
        )
        return event
    
    @override
    def _to_model(self, event: Event) -> EventModel:
        """
        Converte uma entidade de domínio Event em um objeto EventModel para
        persistência no banco de dados, garantindo o tratamento correto do timestamp
        e o mapeamento de campos adicionais para extra_data.

        Args:
            event (Event): Entidade de domínio contendo os dados a serem convertidos.

        Returns:
            EventModel: Instância pronta para ser inserida ou atualizada no banco
            de dados.
        
        Raises:
            ValueError: Caso o timestamp seja informado como string em formato inválido.
        """
        timestamp = event.timestamp
        if isinstance(timestamp, str):
            try:
                timestamp = datetime.fromisoformat(timestamp)
            except ValueError:
                raise ValueError(
                    "Formato de timestamp inválido. Use ISO 8601: YYYY-MM-DDTHH:MM:SS"
                )
        timestamp = timestamp or datetime.now(timezone.utc)

        data = asdict(event)
        extra_data = {
            key: value
            for key, value in data.items()
            if key not in ("id", "animal_id", "event_type", "timestamp")
        }

        event_model = EventModel(
            id=event.id,
            animal_id=event.animal_id,
            event_type=event.event_type.value,
            timestamp=timestamp,
            extra_data=extra_data
        )
        return event_model

    @override
    def list_all(self, event_type: EventType = None, animal_id: int = None) -> list[Event]:
        """
        Recupera todos os eventos registrados no banco, com possibilidade de filtragem
        por tipo de evento e/ou identificador do animal associado.

        Args:
            event_type (EventType): Tipo de evento desejado.
            animal_id (int): Identificador do animal cujos eventos
            devem ser retornados.

        Returns:
            list[Event]: Lista de entidades de domínio correspondentes aos registros
            encontrados no banco, já convertidas via mapeamento de domínio.
        """
        query = self.session.query(EventModel)

        if event_type is not None:
            query = query.filter_by(event_type=event_type.value)

        if animal_id is not None:
            query = query.filter_by(animal_id=animal_id)

        models = query.all()
        events = [self._to_domain(model) for model in models]
        return events