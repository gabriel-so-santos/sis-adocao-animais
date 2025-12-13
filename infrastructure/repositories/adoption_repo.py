from .base_repo import BaseRepository
from infrastructure.db_models.adoption_model import AdoptionModel
from domain.adoptions.adoption import Adoption

class AdoptionRepository(BaseRepository):

    domain_class = Adoption
    
    def __init__(self, session):
        super().__init__(session, AdoptionModel)