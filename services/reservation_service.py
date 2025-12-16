from domain.adoptions.reservation_queue import ReservationQueue
from domain.adoptions.adoption import Adoption
from domain.enums.animal_status import AnimalStatus
from .compatibility_service import CompatibilityService
from .adoption_fee_service import AdoptionFeeService
from datetime import datetime, timedelta
from collections import defaultdict
import json

with open("settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)

queue_duration = settings["policies"]["reservation_duration_hours"]

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
        """
        Retorna as reservas agrupadas por animal e separadas
        entre filas concluídas e em andamento.
        """
        reservations = self.reservation_repo.list_all()
        now = datetime.now()

        grouped = defaultdict(list)

        # Agrupa reservas ativas por animal
        for r in reservations:
            if not r.is_canceled:
                grouped[r.animal_id].append(r)

        finished = {}
        ongoing = {}

        for animal_id, queue in grouped.items():
            
            first = min(queue, key=lambda r: r.timestamp)
            queue_end = first.timestamp + timedelta(hours=queue_duration)

            animal = self.animal_repo.get_by_id(id=animal_id)

            reservations_data = []
            for r in sorted(queue):
                adopter = self.adopter_repo.get_by_id(id=r.adopter_id)

                reservations_data.append({
                    "id": r.id,
                    "timestamp": r.timestamp,
                    "compatibility_rate": r.compatibility_rate,
                    "adopter": adopter
                })

            queue_data = {
                "animal": animal,
                "queue_ending": queue_end,
                "reservations": reservations_data
            }

            # Decide se a fila está concluída ou em andamento
            if now >= queue_end:
                finished[animal_id] = queue_data
            else:
                ongoing[animal_id] = queue_data

        return {
            "finished": finished,
            "ongoing": ongoing
        }

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

        animal = self.animal_repo.get_by_id(animal_id)
        adopter = self.adopter_repo.get_by_id(adopter_id)

        compatibility = CompatibilityService().calculate_rate(animal, adopter)

        had_active_reservations = self.reservation_repo.has_active_reservations(animal_id)

        reservation = ReservationQueue(
            animal_id=animal_id,
            adopter_id=adopter_id,
            compatibility_rate=compatibility
        )
        was_saved = self.reservation_repo.save(reservation)
        if not was_saved:
            raise ValueError("Reserva já existente.")

        if not had_active_reservations:
            self.animal_repo.update_status(
                id=animal_id,
                new_status=AnimalStatus.RESERVED
            )

    def get_queue_ending_time(self, animal_id: int) -> datetime:
        first_reservation = self.reservation_repo.get_first_reservation(animal_id)
        queue_ending = first_reservation.timestamp + timedelta(hours=queue_duration)
        return queue_ending

    def cancel_reservation(self, reservation_id: int):
        self.reservation_repo.cancel_reservation(reservation_id)

        reservation = self.reservation_repo.get_by_id(reservation_id)
        animal_id = reservation.animal_id

        if self.reservation_repo.all_canceled(animal_id):
            self.reservation_repo.clear_queue(animal_id)

            self.animal_repo.update_status(
                id=animal_id,
                new_status=AnimalStatus.AVAILABLE
            )
    
    def finalize_queue(self, animal_id: int):

        if not self.reservation_repo.is_queue_expired(
            animal_id,
            queue_duration
        ):
            return None

        queue = self.reservation_repo.list_active_queue(animal_id)

        if not queue:
            self.animal_repo.update_status(
                id=animal_id,
                new_status=AnimalStatus.AVAILABLE
            )
            return None

        selected = queue[0] 
        return selected
    
    def confirm_adoption(self, reservation_id: int):

        reservation = self.reservation_repo.get_by_id(reservation_id)

        animal_id = reservation.animal_id
        adopter_id = reservation.adopter_id

        self.reservation_repo.clear_queue(animal_id)

        animal = self.animal_repo.get_by_id(id=animal_id)
        fee = AdoptionFeeService().calculate_fee(animal)

        self.animal_repo.update_status(
            id=animal_id,
            new_status=AnimalStatus.ADOPTED
        )

        adoption = Adoption(
            animal_id=animal_id,
            adopter_id=adopter_id,
            fee=fee
        )

        self.adoption_repo.save(adoption)