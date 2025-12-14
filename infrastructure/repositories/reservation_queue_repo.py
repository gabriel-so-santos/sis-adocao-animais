from .base_repo import BaseRepository
from infrastructure.db_models.reservation_queue_model import ReservationQueueModel
from domain.adoptions.reservation_queue import ReservationQueue
from sqlalchemy import exists
from typing import override

class ReservationQueueRepository(BaseRepository):

    domain_class = ReservationQueue
   
    def __init__(self, session):
        super().__init__(session, ReservationQueueModel)
    
    def clear_queue(self, animal_id: int) -> None:
        """
        Remove todas as reservas associadas a um animal.

        Args:
            animal_id (int): ID do animal cujo a reserva está vinculada.

        Returns:
            None
        """
        queue = self.session.query(ReservationQueueModel).filter_by(animal_id=animal_id)
        queue.delete(synchronize_session=False)
        self.session.commit()

    def has_active_reservations(self, animal_id: int) -> bool:
        """
        Verifica se a fila de reservas de um determinado animal tem reservas ativas.

        Args:
            animal_id (int): ID do animal a ser verificado.

        Returns:
            bool: True se houver reservas ativas para o animal,
                False caso contrário.
        """
        query = self.session.query(
            exists().where(ReservationQueueModel.animal_id == animal_id)
        )
        query.scalar()

        return query