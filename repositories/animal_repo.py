from models.animal_model import AnimalModel
import json

from domain.animals.cat import Cat
from domain.animals.dog import Dog

class AnimalRepository:
    def __init__(self, session):
        self.session = session

    def to_domain(self, animal_model: AnimalModel) -> Cat | Dog:
        """Converte o Model (SQL) em entidades de domínio"""
        from domain.animals.animal import Species, Gender, Size
        from domain.animals.animal_status import AnimalStatus
        
        species = Species[animal_model.species]
        extra_data = animal_model.extra_data or {}

        if species == Species.CAT:   
            animal = Cat(
                id=animal_model.id,
                species=species,
                breed=animal_model.breed,
                name=animal_model.name,
                gender=Gender[animal_model.gender],
                age_months=animal_model.age_months,
                size=Size[animal_model.size],
                temperament=json.loads(animal_model.temperament),
                status=AnimalStatus[animal_model.status],
                is_hypoallergenic=extra_data.get("is_hypoallergenic", False)
            )

        else:
            animal = Dog(
                id=animal_model.id,
                species=species,
                breed=animal_model.breed,
                name=animal_model.name,
                gender=Gender[animal_model.gender],
                age_months=animal_model.age_months,
                size=Size[animal_model.size],
                temperament=json.loads(animal_model.temperament),
                status=AnimalStatus[animal_model.status],
                needs_walk=extra_data.get("needs_walk", False)
            )

        return animal

    # ---- Create ----
    def save(self, animal: Cat | Dog) -> AnimalModel:
        """Salva uma entidade Animal no banco"""

        extra_data = {}

        if isinstance(animal, Dog):
            extra_data["needs_walk"] = animal.needs_walk

        if isinstance(animal, Cat):
            extra_data["is_hypoallergenic"] = animal.is_hypoallergenic


        animal_db = AnimalModel(
            id=animal.id, 
            species=animal.species.name,        # Enum -> str
            breed=animal.breed,
            name=animal.name,
            gender=animal.gender.name,          # Enum -> str
            age_months=animal.age_months,
            size=animal.size.name,              #Enum -> str
            temperament=json.dumps(animal.temperament),
            status=animal.status.name,          # Enum -> str
            extra_data=extra_data
        )

        self.session.add(animal_db)
        self.session.commit()
        self.session.refresh(animal_db)
        return animal_db

    # ---- Read ----
    def list_all(self) -> list[AnimalModel]:
        """Retorna uma lista de todos os anmais cadastrados no banco"""
        return self.session.query(AnimalModel).all()

    def get_by_id(self, id: int) -> AnimalModel:
        """Retorna um animal cadastrado no banco"""
        return self.session.get(AnimalModel, id)

    # ---- Update ----
    def update(self, animal) -> AnimalModel | None:
        """Atualiza um registro existente no banco a partir de um objeto de domínio"""
        animal_db = self.session.get(AnimalModel, animal.id)

        if not animal_db:
            return None

        animal_db.species = animal.species.name
        animal_db.breed = animal.breed
        animal_db.name = animal.name
        animal_db.gender = animal.gender.name
        animal_db.age_months = animal.age_months
        animal_db.size = animal.size.name
        animal_db.temperament = json.dumps(animal.temperament)
        animal_db.status = animal.status.name

        self.session.commit()
        self.session.refresh(animal_db)
        return animal_db

    # ---- Delete ----
    def delete_by_id(self, id: int) -> bool:
        animal_db = self.session.get(AnimalModel, id)

        if not animal_db:
            return False

        self.session.delete(animal_db)
        self.session.commit()
        return True