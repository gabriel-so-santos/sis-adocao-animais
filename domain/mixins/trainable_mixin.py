from domain.events.events import TrainingEvent

class TrainableMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._trainings: list[TrainingEvent] = []

    @property
    def trainings(self) -> list[TrainingEvent]:
        return self._trainings