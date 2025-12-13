from .base_repo import BaseRepository
from typing import override

from infrastructure.db_models.adopter_model import AdopterModel
from domain.people.adopter import Adopter, HousingType

class AdopterRepository(BaseRepository):
   
    def __init__(self, session):
        super().__init__(session, AdopterModel)
    
    @override
    def _to_domain(self, adopter_model: AdopterModel) -> Adopter:
        """
        Converte um objeto AdopterModel (SQLAlchemy) em uma entidade de domínio Adopter.

        Args:
            adopter_model (AdopterModel): Instância do modelo persistido no banco de dados.

        Returns:
            Adopter: Entidade de domínio correspondente.
        """
        adopter = Adopter(
            id=adopter_model.id,
            name=adopter_model.name,
            age=adopter_model.age,
            timestamp=adopter_model.timestamp,

            housing_type=HousingType[adopter_model.housing_type],    
            usable_area=adopter_model.usable_area,
            has_pet_experience=adopter_model.has_pet_experience,
            has_children_at_home=adopter_model.has_children_at_home,
            has_other_animals=adopter_model.has_other_animals
        )
        return adopter
    
    @override
    def _to_model(self, adopter: Adopter) -> AdopterModel:
        """
        Converte uma entidade de domínio Adopter em um objeto AdopterModel (SQLAlchemy).

        Args:
            adopter (Adopter): Entidade de domínio.

        Returns:
            AdopterModel: Instância do modelo persistido no banco de dados.
        """
        adopter_model = AdopterModel(
            id=adopter.id,
            timestamp=adopter.timestamp,
            name=adopter.name,
            age=adopter.age,
            housing_type=adopter.housing_type.value,
            usable_area=adopter.usable_area,
            has_pet_experience=adopter.has_pet_experience,
            has_children_at_home=adopter.has_children_at_home,
            has_other_animals=adopter.has_other_animals
        )
        return adopter_model