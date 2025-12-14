from .base_repo import BaseRepository
from infrastructure.db_models.adoption_return_model import AdoptionReturnModel
from domain.adoptions.adoption_return import AdoptionReturn
from datetime import datetime

class AdoptionReturnRepository(BaseRepository):

    domain_class = AdoptionReturn
    
    def __init__(self, session):
        super().__init__(session, AdoptionReturnModel)

    def has_returned_adoption(self, adoption_id: int) -> bool:
        """
        Verifica se uma adoção já possui uma devolução registrada.

        Args:
            adoption_id (int): ID da adoção a ser verificada.

        Returns:
            bool: True se já existir uma devolução associada à adoção,
                  False caso contrário.
        """
        return (
            self.session.query(AdoptionReturnModel)
            .filter_by(adoption_id=adoption_id)
            .first()
            is not None
        )
    
    def get_timestamp(self, id: int = None, adoption_id: int = None) -> datetime:
        """
        Retorna o timestamp da devolução associada a uma adoção.

        Args:
            id (int): Identificador da devolução a ser verificada.
            adoption_id (int): Identificador da adoção a ser verificada.

        Returns:
            datetime | None: Data e hora da devolução, caso exista uma devolução
            registrada para a adoção informada; caso contrário, retorna None.
        """
        if id is None and adoption_id is None:
            raise ValueError("Informe 'id' ou 'adoption_id'.")

        query = self.session.query(AdoptionReturnModel)

        if id is not None:
            query = query.filter_by(id=id)
        else:
            query = query.filter_by(adoption_id=adoption_id)

        result = query.first()
        return result.timestamp if result else None
    
    def get_return_reason(self, adoption_id: int) -> str | None:
        """
        Retorna o motivo (reason) da devolução associada a uma adoção.

        Args:
            adoption_id (int): Identificador da adoção.

        Returns:
            str | None: Texto com o motivo da devolução, caso exista;
            None se não houver devolução registrada.
        """
        result = (
            self.session
            .query(AdoptionReturnModel.reason)
            .filter_by(adoption_id=adoption_id)
            .first()
        )

        return result.reason if result else None