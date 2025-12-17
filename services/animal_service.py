from datetime import datetime
from domain.animals.cat import Cat
from domain.animals.dog import Dog

from domain.enums.animal_enums import Species, Gender, Size
from domain.enums.animal_status import AnimalStatus

from domain.events.animal_events import QuarentineEvent, VaccineEvent, TrainingEvent

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
            species=species,
            breed=form_data["breed"].strip().capitalize(),
            name=form_data["name"].strip().capitalize(),
            gender=Gender[form_data["gender"].upper()],
            age_months=int(form_data["age_months"]),
            size=Size[form_data["size"].upper()],
            temperament=temperament,
            status=AnimalStatus.AVAILABLE
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
                timestamp=datetime.now()
            )
            self.event_repo.save(event)

    def __parse_date(self, date_str: str):
        return datetime.strptime(date_str, "%Y-%m-%d")

    # ---------------- VACCINE ----------------

    def prepare_vaccine_form(self, animal_id):
        return self.get_animal(animal_id)

    def register_vaccine(self, animal_id, form_data):
        date = self.__parse_date(form_data["vaccine_date"])

        vaccine = VaccineEvent(
            id=None,
            animal_id=animal_id,
            timestamp=date,
            vaccine_name=form_data["vaccine_name"].strip(),
            veterinarian=form_data.get("veterinarian", "").strip().capitalize()
        )
        self.event_repo.save(vaccine)

    # ---------------- TRAINING ----------------

    def prepare_training_form(self, animal_id):
        return self.get_animal(animal_id)

    def register_training(self, animal_id, form_data):
        date = self.__parse_date(form_data["vaccine_date"])

        training = TrainingEvent(
            id=None,
            animal_id=animal_id,
            timestamp=date,
            duration_min=int(form_data.get("duration_min") or 0),
            training_type=form_data["training_type"],
            trainer=form_data["trainer"].strip().capitalize(),
            notes=form_data["notes"]
        )
        self.event_repo.save(training)


    def get_by_id(self, animal_id: int):
        return self.animal_repo.get_by_id(animal_id)

    from domain.enums.animal_enums import Gender, Size

    def update(self, animal_id, **kwargs):
        
        animal_model = self.animal_repo.get_by_id(animal_id)
        if not animal_model:
            raise ValueError("Animal não encontrado")

        if "gender" in kwargs:
            kwargs["gender"] = Gender(kwargs["gender"].upper())  
        
        if "size" in kwargs:
            kwargs["size"] = Size(kwargs["size"].upper())  

        for key, value in kwargs.items():
            if hasattr(animal_model, key):
                setattr(animal_model, key, value)

        self.animal_repo.update(animal_model)
        return animal_model
