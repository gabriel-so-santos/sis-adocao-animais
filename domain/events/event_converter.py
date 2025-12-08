from datetime import datetime
from domain.events.events import (
    TrainingEvent, VaccineEvent, ReservationEvent,
    AdoptionEvent, ReturnEvent, Event, EventType
)

class EventConverter:

    @staticmethod
    def convert_to_domain_event(
        id: int,
        animal_id: int,
        event_type: EventType,
        timestamp,
        extra_data: dict
    ) -> Event:
        """
        Converte dados brutos de banco em um objeto de domínio específico.
        """

        kwargs = {
            "id": id,
            "animal_id": animal_id,
            "timestamp": timestamp
        }
        extra_data = extra_data or {}

        if event_type == EventType.VACCINE:
            kwargs["vaccine_name"] = str(extra_data.get("vaccine_name", ""))
            return VaccineEvent(**kwargs)

        if event_type == EventType.TRAINING:
            kwargs["duration_min"] = int(extra_data.get("duration_min", 0))
            kwargs["notes"] = str(extra_data.get("notes", ""))
            return TrainingEvent(**kwargs)

        if event_type == EventType.RESERVATION:
            kwargs["adopter_id"] = int(extra_data["adopter_id"])
            return ReservationEvent(**kwargs)

        if event_type == EventType.ADOPTION:
            kwargs["adopter_id"] = int(extra_data["adopter_id"])
            kwargs["fee"] = float(extra_data["fee"])
            return AdoptionEvent(**kwargs)

        if event_type == EventType.RETURN:
            kwargs["adoption_id"] = int(extra_data["adoption_id"])
            kwargs["notes"] = str(extra_data.get("notes", ""))
            return ReturnEvent(**kwargs)

        # Evento desconhecido → retorna evento genérico
        return Event(**kwargs)