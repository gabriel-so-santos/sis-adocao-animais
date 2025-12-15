from domain.events.animal_events import VaccineEvent

class VaccinableMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._vaccines: list[VaccineEvent] = []
        self.is_vaccineable = True

    @property
    def vaccines(self) -> list[VaccineEvent]:
        return self._vaccines
    