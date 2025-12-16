from .base_repo import BaseRepository
from infrastructure.db_models.reservation_queue_model import ReservationQueueModel
from domain.adoptions.reservation_queue import ReservationQueue
from sqlalchemy import asc
from datetime import datetime, timedelta

class ReservationQueueRepository(BaseRepository):

    domain_class = ReservationQueue
   
    def __init__(self, session):
        super().__init__(session, model_class=ReservationQueueModel)
    
    # ---- Read ----

    def has_active_reservations(self, animal_id: int) -> bool:
        """
        Verifica se a fila de reservas de um determinado animal tem reservas ativas.

        Args:
            animal_id (int): ID do animal a ser verificado.

        Returns:
            bool: True se houver reservas ativas para o animal;
                False caso contrário.
        """
        models = self.session.query(self.model_class).filter_by(animal_id=animal_id).all()

        for model in models:
            if model.is_canceled == False:
                return True
            
        return False
    
    def all_canceled(self, animal_id: int) -> bool:
        models = self.session.query(self.model_class).filter_by(animal_id=animal_id).all()

        if not models:
            return True

        return all(m.is_canceled for m in models)

    
    def get_first_reservation(self, animal_id: int) -> ReservationQueue | None:
        """
        Retorna a primeira reserva realizada para um determinado animal.

        A primeira reserva é definida como a reserva mais antiga
        (menor timestamp) associada ao animal.

        Args:
            animal_id (int): ID do animal.

        Returns:
            ReservationQueue | None: A primeira reserva encontrada;
            None caso não exista nenhuma reserva.
        """
        model = (
            self.session
            .query(ReservationQueueModel)
            .filter_by(animal_id=animal_id)
            .order_by(asc(ReservationQueueModel.timestamp))
            .first()
        )

        if not model:
            return None

        return self._to_domain(model)
    
    def is_queue_expired(self, animal_id: int, duration_hours: int) -> bool:
        first = self.get_first_reservation(animal_id)

        if not first:
            return False

        expiration = first.timestamp + timedelta(hours=duration_hours)
        return datetime.now() >= expiration
        
    def list_active_queue(self, animal_id: int) -> list[ReservationQueue]:
        """
        Retorna a fila ativa de reservas de um animal,
        ordenada por prioridade.
        """
        models = (
            self.session
            .query(self.model_class)
            .filter_by(animal_id=animal_id, is_canceled=False)
            .all()
        )
        queue = [self._to_domain(m) for m in models]
        queue.sort()    # Using __lt__
        return queue
        
    # ---- Update ----

    def cancel_reservation(self,id: int) -> bool:
        """
        Altera o status da reserva para cancelado.

        Args:
            id (int): ID da reserva.

        Returns:
            bool: True se a reserva existir;
                False caso contário.
        """
        reservation_model = self.session.get(ReservationQueueModel, id)

        if not reservation_model:
            return False

        reservation_model.is_canceled = True
        self.session.commit()
        self.session.refresh(reservation_model)
        return True
    
    # ---- Delete ----
    
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