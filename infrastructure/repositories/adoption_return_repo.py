from .base_repo import BaseRepository
from infrastructure.db_models.adoption_return_model import AdoptionReturnModel
from domain.adoptions.adoption_return import AdoptionReturn

class AdoptionReturnRepository(BaseRepository):

    domain_class = AdoptionReturn
    
    def __init__(self, session):
        super().__init__(session, AdoptionReturnModel)