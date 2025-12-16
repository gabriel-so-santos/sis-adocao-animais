from sqlalchemy import(
    UniqueConstraint, Column, Integer, Float, ForeignKey, DateTime, Boolean, func
)
from sqlalchemy.orm import relationship
from infrastructure.database.db_connection import Base

class ReservationQueueModel(Base):
    __tablename__ = "reservation_queue"

    __table_args__ = (
        UniqueConstraint(
            "animal_id", "adopter_id",
        ),  # Single-element tuple required by SQLAlchemy
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    animal_id = Column(Integer, ForeignKey("animals.id", ondelete="CASCADE"), nullable=False)
    adopter_id = Column(Integer, ForeignKey("adopters.id", ondelete="CASCADE"), nullable=False)
    compatibility_rate = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    is_canceled = Column(Boolean, nullable=False)

    # -------------------------- RELATIONSHIPS --------------------------

    animal = relationship("AnimalModel", back_populates="reservation_queue")

    adopter = relationship("AdopterModel", back_populates="reservation_queue")