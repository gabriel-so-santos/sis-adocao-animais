from models.animal_model import AnimalModel
import json

class AnimalRepository:
    def __init__(self, session):
        self.session = session

    def to_domain(self, animal_model: AnimalModel):
        """Converte o Model (SQL) em uma entidade de domínio"""
        from domain.animals.animal import Animal, Species, Gender, Size
        from domain.animals.animal_status import AnimalStatus
        
        return Animal(
            id=animal_model.id,
            species=Species[animal_model.species],
            breed=animal_model.breed,
            name=animal_model.name,
            gender=Gender[animal_model.gender], 
            age_months=animal_model.age_months,
            size=Size[animal_model.size],       
            temperament=json.loads(animal_model.temperament),
            status=AnimalStatus[animal_model.status] 
        )

    # ---- Create ----
    def save(self, animal) -> AnimalModel:
        """Salva uma entidade Animal no banco"""

        animal_db = AnimalModel(
            id=animal.id, 
            species=animal.species.name,  # Enum -> str
            breed=animal.breed,
            name=animal.name,
            gender=animal.gender.name,    # Enum -> str
            age_months=animal.age_months,
            size=animal.size.name,        # Enum -> str
            temperament=json.dumps(animal.temperament),
            status=animal.status.name,    # Enum -> str
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
    def update(self, animal) -> AnimalModel|None:
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