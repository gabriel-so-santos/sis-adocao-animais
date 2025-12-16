from dataclasses import dataclass, field
from datetime import datetime
from domain.enums.event_type import EventType
from domain.people.adopter import Adopter

@dataclass
class Event:
    id: int 
    animal_id: int
    timestamp: datetime 

    event_type: EventType = field(init=False, default=None)

    def __lt__(self, e: "Event") -> bool:

        if self.timestamp != e.timestamp:
            return self.timestamp < e.timestamp
        
        if self.id != e.id:
            return self.id < e.id

        return self.event_type.value < e.event_type.value

# ---- Eventos específicos ----

@dataclass
class TrainingEvent(Event):
    duration_min: int
    training_type: str
    trainer: str
    notes: str

    event_type: EventType = field(init=False, default=EventType.TRAINING)


@dataclass
class VaccineEvent(Event):
    vaccine_name: str
    veterinarian: str
    
    event_type: EventType = field(init=False, default=EventType.VACCINE)


@dataclass
class AdoptionEvent(Event):
    adopter: Adopter
    fee: float

    event_type: EventType = field(init=False, default=EventType.ADOPTION)


@dataclass
class ReturnEvent(Event):
    adoption_id: int
    reason: str

    event_type: EventType = field(init=False, default=EventType.RETURN)

@dataclass
class QuarentineEvent(Event):

    event_type: EventType = field(init=False, default=EventType.QUARENTINE)