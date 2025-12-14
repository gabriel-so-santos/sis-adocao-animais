from sqlalchemy import(
    UniqueConstraint, Column, String, Integer, DateTime, func, JSON
)
from sqlalchemy.orm import relationship
from infrastructure.database.db_connection import Base

class AnimalModel(Base):
    __tablename__ = "animals"

    __table_args__ = (
        UniqueConstraint(
            "species", "breed",
            "name", "gender",
            "age_months", "size"
        ),  # Single-element tuple required by SQLAlchemy
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    species = Column(String, nullable=False)
    breed = Column(String, nullable=False)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    age_months = Column(Integer, nullable=False)
    size = Column(String, nullable=False)
    temperament = Column(String, nullable=False)
    status = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False, server_default=func.now())

    extra_data = Column(JSON, nullable=True, default={})

    # -------------------------- RELATIONSHIPS --------------------------

    events = relationship("EventModel", back_populates="animal", cascade="all, delete")

    reservation_queue = relationship(
        "ReservationQueueModel", back_populates="animal", cascade="all, delete-orphan"
    )

    adoptions = relationship("AdoptionModel", back_populates="animal")
    
    