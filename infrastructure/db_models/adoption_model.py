from sqlalchemy import(
    UniqueConstraint, Column, Integer, Float, ForeignKey, DateTime, func
)
from sqlalchemy.orm import relationship
from infrastructure.database.db_connection import Base

class AdoptionModel(Base):
    __tablename__ = "adoptions"

    __table_args__ = (
        UniqueConstraint(
            "animal_id", "adopter_id", "timestamp"
        ),  # Single-element tuple required by SQLAlchemy
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    animal_id = Column(Integer, ForeignKey("animals.id"), nullable=False)
    adopter_id = Column(Integer, ForeignKey("adopters.id"), nullable=False)
    fee = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    # -------------------------- RELATIONSHIPS --------------------------

    animal = relationship("AnimalModel", back_populates="adoptions")

    adopter = relationship("AdopterModel", back_populates="adoptions")

    adoption_return = relationship(
        "AdoptionReturnModel", uselist=False,
        back_populates="adoption", cascade="all, delete-orphan"
    )