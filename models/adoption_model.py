from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import Base  
from datetime import datetime, timezone

class AdoptionModel(Base):
    __tablename__ = "adoptions"

    id = Column(Integer, primary_key=True, index=True)
    adopter_id = Column(Integer, ForeignKey("adopters.id"))
    animal_id = Column(Integer, ForeignKey("animals.id"))
    fee = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    adopter = relationship("AdopterModel", back_populates="adoptions")
    animal = relationship("AnimalModel", back_populates="adoptions")