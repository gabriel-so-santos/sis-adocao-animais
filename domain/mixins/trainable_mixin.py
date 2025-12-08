from domain.events.events import TrainingEvent

class TrainableMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._trainings: list[TrainingEvent] = []
        self.is_trainable = True

    @property
    def trainings(self) -> list[TrainingEvent]:
        return self._trainings