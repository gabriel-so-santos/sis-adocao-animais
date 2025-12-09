from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class EventType(Enum):
    RESERVATION = "RESERVATION" 
    ADOPTION = "ADOPTION"
    RETURN = "RETURN"
    TRAINING = "TRAINING"
    VACCINE ="VACCINE" 

@dataclass
class Event:
    id: int
    animal_id: int
    timestamp: datetime

    event_type: EventType = field(init=False, default=None)


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
class ReservationEvent(Event):
    adopter_id: int

    event_type: EventType = field(init=False, default=EventType.RESERVATION)


@dataclass
class AdoptionEvent(Event):
    adopter_id: int
    fee: float

    event_type: EventType = field(init=False, default=EventType.ADOPTION)


@dataclass
class ReturnEvent(Event):
    adoption_id: int
    notes: str

    event_type: EventType = field(init=False, default=EventType.RETURN)