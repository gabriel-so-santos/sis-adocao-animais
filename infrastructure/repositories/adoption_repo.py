from .base_repo import BaseRepository
from infrastructure.db_models.adoption_model import AdoptionModel
from domain.adoptions.adoption import Adoption

class AdoptionRepository(BaseRepository):

    domain_class = Adoption
    
    def __init__(self, session):
        super().__init__(session, model_class=AdoptionModel)

    def get_latest_by_animal(self, animal_id: int) -> Adoption | None:
        """
        Recupera a adoção mais recente associada a um animal.

        Args:
            animal_id (int): Identificador do animal cuja adoção
                mais recente deve ser recuperada.

        Returns:
            Adoption | None: Entidade de domínio da adoção mais recente
            do animal, caso exista; caso contrário, retorna None.
        """
        model = (
            self.session
            .query(AdoptionModel)
            .filter_by(animal_id=animal_id)
            .order_by(AdoptionModel.id.desc())
            .first()
        )
        return self._to_domain(model)
    
    def list_by_animal(self, animal_id: int) -> list[AdoptionModel]:
        """
        Retorna todas as adoções (AdoptionModel) associadas a um animal específico.

        Args:
            animal_id (int): Identificador do animal cujas adoções
                devem ser listadas.

        Returns:
            list[AdoptionModel]: Lista de modelos (SQLAlchemy) de adoções do animal 
            ordenada cronologicamente. Retorna uma lista vazia caso não existam adoções registradas.
        """
        return (
            self.session.query(AdoptionModel)
            .filter_by(animal_id=animal_id)
            .order_by(AdoptionModel.timestamp)
            .all()
        )
