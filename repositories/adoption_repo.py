from models.adoption_model import AdoptionModel
from domain.adoption.adoption import Adoption
from datetime import datetime, timezone

class AdoptionRepository():
    
    def __init__(self, session):
        self.session = session

    def to_domain(self, adoption_model: AdoptionModel) -> Adoption:
        return Adoption(
            id = adoption_model.id,
            adopter_id = adoption_model.adopter_id,
            animal_id = adoption_model.animal_id,
            fee = adoption_model.fee,
            created_at = adoption_model.created_at,
        )

    # ---- Create ----
    def save(self, adoption: Adoption) -> AdoptionModel:
        adoption_db = AdoptionModel(
            adopter_id = adoption.adopter_id,
            animal_id = adoption.animal_id,
            fee = adoption.fee,
            created_at = adoption.created_at or datetime.now(timezone.utc),
        )

        self.session.add(adoption_db)
        self.session.commit()
        self.session.refresh(adoption_db)

        return adoption_db

    # ---- Read ----
    def list_all(self) -> list[AdoptionModel]:
        return self.session.query(AdoptionModel).all()

    def get_by_id(self, id: int) -> AdoptionModel:
        return self.session.get(AdoptionModel, id)

    # ---- Update ----
    def update(self, adoption: Adoption) -> AdoptionModel:
        adoption_db = self.session.get(AdoptionModel, adoption.id)

        if not adoption_db:
            return None

        adoption_db.adopter_id = adoption.adopter_id
        adoption_db.animal_id = adoption.animal_id
        adoption_db.fee = adoption.fee

        self.session.commit()
        self.session.refresh(adoption_db)
        return adoption_db

    # ---- Delete ----
    def delete_by_id(self, id: int) -> bool:
        adoption_db = self.session.get(AdoptionModel, id)

        if not adoption_db:
            return False

        self.session.delete(adoption_db)
        self.session.commit()
        return True