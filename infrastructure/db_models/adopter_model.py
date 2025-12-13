from sqlalchemy import (
    UniqueConstraint, Column, Integer, String, Boolean, Float, DateTime, func
)
from sqlalchemy.orm import relationship
from infrastructure.database.db_connection import Base

class AdopterModel(Base):
    __tablename__ = "adopters"

    __table_args__ = (
        UniqueConstraint(
            "name", "age",
            "housing_type", "usable_area",
            "has_pet_experience", "has_children_at_home", "has_other_animals"
        ),  # Single-element tuple required by SQLAlchemy
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    housing_type = Column(String, nullable=False)         
    usable_area = Column(Float, nullable=False)
    has_pet_experience = Column(Boolean, nullable=False)
    has_children_at_home = Column(Boolean, nullable=False)
    has_other_animals = Column(Boolean, nullable=False)
    timestamp = Column(DateTime, nullable=False, server_default=func.now())

    # -------------------------- RELATIONSHIPS --------------------------

    reservation_queue = relationship(
        "ReservationQueueModel", back_populates="adopter", cascade="all, delete-orphan"
    )

    adoptions = relationship("AdoptionModel", back_populates="adopter")