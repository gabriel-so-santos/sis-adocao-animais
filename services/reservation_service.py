from domain.adoptions.reservation_queue import ReservationQueue
from domain.adoptions.adoption import Adoption
from domain.enums.animal_status import AnimalStatus

class ReservationService:

    def __init__(
        self,
        reservation_repo,
        animal_repo,
        adopter_repo,
        adoption_repo
    ):
        self.reservation_repo = reservation_repo
        self.animal_repo = animal_repo
        self.adopter_repo = adopter_repo
        self.adoption_repo = adoption_repo

    def list_reservations(self):
        reservations = self.reservation_repo.list_all()

        result = []
        for r in reservations:
            animal = self.animal_repo.get_by_id(id=r.animal_id)
            adopter = self.adopter_repo.get_by_id(id=r.adopter_id)

            result.append({
                "id": r.id,
                "date": r.timestamp,
                "animal": animal,
                "adopter": adopter
            })

        return result

    def prepare_reservation_form(self, animal_id=None, adopter_id=None):
        animals = adopters = None
        selected_animal = selected_adopter = None

        if animal_id:
            selected_animal = self.animal_repo.get_by_id(animal_id)
        else:
            animals = self.animal_repo.list_reservable_animals()

        if adopter_id:
            selected_adopter = self.adopter_repo.get_by_id(adopter_id)
        else:
            adopters = self.adopter_repo.list_all()

        return {
            "animals": animals,
            "adopters": adopters,
            "selected_animal": selected_animal,
            "selected_adopter": selected_adopter
        }

    def create_reservation(self, animal_id: int, adopter_id: int):
        reservation = ReservationQueue(
            animal_id=animal_id,
            adopter_id=adopter_id,
            compatibility_rate=50,
        )

        was_saved = self.reservation_repo.save(reservation)

        if not was_saved:
            raise ValueError("Esta reserva já foi cadastrada.")

        self.animal_repo.update_status(
            id=animal_id,
            new_status=AnimalStatus.RESERVED
        )

    def confirm_reservation(self, reservation_id: int):
        reservation = self.reservation_repo.get_by_id(id=reservation_id)

        animal_id = reservation.animal_id
        adopter_id = reservation.adopter_id

        self.reservation_repo.clear_queue(animal_id=animal_id)

        self.animal_repo.update_status(
            id=animal_id,
            new_status=AnimalStatus.ADOPTED
        )

        adoption = Adoption(
            animal_id=animal_id,
            adopter_id=adopter_id,
            fee=0,
        )

        self.adoption_repo.save(adoption)

    def cancel_reservation(self, reservation_id: int):
        self.reservation_repo.delete_by(id=reservation_id)