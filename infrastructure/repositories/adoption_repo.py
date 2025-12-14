from .base_repo import BaseRepository
from infrastructure.db_models.adoption_model import AdoptionModel
from domain.adoptions.adoption import Adoption
from typing import override

class AdoptionRepository(BaseRepository):

    domain_class = Adoption
    
    def __init__(self, session):
        super().__init__(session, model_class=AdoptionModel)

    def get_by_animal_id(self, animal_id: int) -> Adoption | None:
        model = (
            self.session
            .query(AdoptionModel)
            .filter_by(animal_id=animal_id)
            .first()
        )
        return self._to_domain(model)