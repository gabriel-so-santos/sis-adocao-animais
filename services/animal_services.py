from domain.animals.cat import Cat
from domain.animals.dog import Dog

from domain.enums.animal_enums import Species, Gender, Size
from domain.enums.animal_status import AnimalStatus

from domain.events.animal_events import QuarentineEvent

class AnimalService:

    def __init__(self, animal_repo, event_repo):
        self.animal_repo = animal_repo
        self.event_repo = event_repo

    def list_animals(self) -> list[Cat | Dog]:
        return self.animal_repo.list_all()

    def get_animal(self, animal_id) -> Cat | Dog:
        return self.animal_repo.get_by_id(id=animal_id)

    def create_animal(self, form_data) -> bool:
        species = Species[form_data["species"].upper()]

        temperament = [
            t.strip().capitalize()
            for t in form_data["temperament"].split(",")
            if t.strip()
        ]

        shared_args = dict(
            id=None,
            species=species,
            breed=form_data["breed"].strip().capitalize(),
            name=form_data["name"].strip().capitalize(),
            gender=Gender[form_data["gender"].upper()],
            age_months=int(form_data["age_months"]),
            size=Size[form_data["size"].upper()],
            temperament=temperament,
            status=AnimalStatus[form_data["status"].upper()]
        )

        if species == Species.CAT:
            animal = Cat(
                **shared_args,
                is_hypoallergenic=form_data.get("is_hypoallergenic") == "true"
            )
        else:
            animal = Dog(
                **shared_args,
                needs_walk=form_data.get("needs_walk") == "true"
            )

        was_saved = self.animal_repo.save(animal)
        return was_saved

    def change_status(self, animal_id: int, status_str: str):
        new_status = AnimalStatus[status_str.upper()]

        self.animal_repo.update_status(animal_id, new_status)

        if new_status == AnimalStatus.QUARANTINE:
            event = QuarentineEvent(
                id=None,
                animal_id=animal_id,
                timestamp=None
            )
            self.event_repo.save(event)