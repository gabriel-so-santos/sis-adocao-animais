from domain.events.animal_events import Event, AdoptionEvent, ReturnEvent

class TimelineService:

    def __init__(
        self,
        adoption_repo,
        adoption_return_repo,
        event_repo,
        adopter_repo
    ):
        self.adoption_repo = adoption_repo
        self.adoption_return_repo = adoption_return_repo
        self.event_repo = event_repo
        self.adopter_repo = adopter_repo

    def build_animal_timeline(self, animal_id: int) -> list[Event]:
        """
        Constrói a linha do tempo completa de um animal, agregando
        eventos genéricos, adoções e devoluções, ordenados
        cronologicamente.

        Args:
            animal_id (int): Identificador do animal.

        Returns:
            list[Event]: Lista de eventos ordenados por timestamp.
        """
        timeline = list()

        # Vaccine / Training / Quarentine
        generic_events = self.event_repo.list_by(animal_id=animal_id)
        timeline.extend(generic_events)

        # Adoptions
        adoptions = self.adoption_repo.list_by_animal(animal_id)

        for adoption in adoptions:

            adopter = self.adopter_repo.get_by_id(adoption.adopter_id)

            adoption_event = AdoptionEvent(
                id=adoption.id,
                animal_id=adoption.animal_id,
                adopter=adopter,
                fee=adoption.fee,
                timestamp=adoption.timestamp
            )
            timeline.append(adoption_event)

            # Adoption Returns
            ret_timestamp = self.adoption_return_repo.get_timestamp(
                adoption_id=adoption.id
            )
            ret_reason = self.adoption_return_repo.get_return_reason(
                adoption_id=adoption.id
            )

            if ret_timestamp:
                return_event = ReturnEvent(
                    id=adoption.id,
                    animal_id=animal_id,
                    adoption_id=adoption.id,
                    reason=ret_reason,
                    timestamp=ret_timestamp
                )
                timeline.append(return_event)
        timeline.sort()

        return timeline