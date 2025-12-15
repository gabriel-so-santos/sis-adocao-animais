from domain.adoptions.adoption_return import AdoptionReturn
from domain.enums.animal_status import AnimalStatus

class AdoptionService:

    def __init__(
        self,
        adoption_repo,
        adoption_return_repo,
        animal_repo,
        adopter_repo
    ):
        self.adoption_repo = adoption_repo
        self.adoption_return_repo = adoption_return_repo
        self.animal_repo = animal_repo
        self.adopter_repo = adopter_repo

    def list_adoptions(self):
        adoptions = self.adoption_repo.list_all()

        active_adoptions = []
        returned_adoptions = []

        for adoption in adoptions:
            animal = self.animal_repo.get_by_id(id=adoption.animal_id)
            adopter = self.adopter_repo.get_by_id(id=adoption.adopter_id)

            has_returned = self.adoption_return_repo.has_returned_adoption(adoption.id)

            if not has_returned:
                active_adoptions.append({
                    "id": adoption.id,
                    "timestamp": adoption.timestamp,
                    "fee": adoption.fee,
                    "animal": animal,
                    "adopter": adopter,
                })
            else:
                returned_adoptions.append({
                    "id": adoption.id,
                    "adoption_timestamp": adoption.timestamp,
                    "return_timestamp": self.adoption_return_repo.get_timestamp(
                        adoption_id=adoption.id
                    ),
                    "fee": adoption.fee,
                    "animal": animal,
                    "adopter": adopter,
                })

        return {
            "active": active_adoptions,
            "returned": returned_adoptions
        }

    def prepare_return_form(self, animal_id: int):
        return self.animal_repo.get_by_id(id=animal_id)

    def register_return(self, animal_id: int, reason: str):
        adoption = self.adoption_repo.get_latest_by_animal(animal_id)

        adoption_return = AdoptionReturn(
            adoption_id=adoption.id,
            reason=reason
        )

        self.adoption_return_repo.save(adoption_return)

        self.animal_repo.update_status(
            id=animal_id,
            new_status=AnimalStatus.RETURNED
        )
