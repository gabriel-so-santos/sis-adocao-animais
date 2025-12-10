from datetime import datetime, timezone
from dataclasses import asdict
from infrastructure.models.event_model import EventModel
from domain.events.events import EventType

class EventRepository:
    def __init__(self, session):
        self.session = session

    def to_domain(self, event_model: EventModel):
        """Converte o Model (SQL) em entidades de domínio"""
        from domain.events.event_converter import EventConverter

        timestamp = event_model.timestamp
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)

        return EventConverter.convert_to_domain_event(
            id=event_model.id,
            animal_id=event_model.animal_id,
            event_type=EventType[event_model.event_type],
            timestamp=timestamp,
            extra_data=event_model.extra_data or {}
        )

    def save(self, event):
        """Salva objeto de domínio no banco, mapeando campos extras para extra_data"""
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
        extra_data = {k: v for k, v in data.items() if k not in ("id", "animal_id", "event_type", "timestamp")}

        event_db = EventModel(
            id=event.id,
            animal_id=event.animal_id,
            event_type=event.event_type.value,
            timestamp=timestamp,
            extra_data=extra_data
        )

        self.session.add(event_db)
        self.session.commit()
        return event_db

    def list_by_type(self, event_type: EventType, animal_id: int = None) -> list[EventModel]:
        """Retorna todos os eventos do tipo especificado"""

        query = self.session.query(EventModel).filter_by(event_type=event_type.value)

        if animal_id is not None:
            query = query.filter_by(animal_id=animal_id)

        return query.all()

    def get_by_id(self, id: int) -> EventModel:
        """Retorna um evento pelo ID"""
        return self.session.get(EventModel, id)
    
     # ---- Delete ----
    def delete_by_id(self, id: int) -> bool:
        event_db = self.session.get(EventModel, id)

        if not event_db:
            return False

        self.session.delete(event_db)
        self.session.commit()
        return True