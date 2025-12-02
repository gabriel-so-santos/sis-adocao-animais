from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from models.base_repo import Base

class AnimalModel(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    species = Column(String)
    breed = Column(String)
    name = Column(String)
    gender = Column(String)
    age_months = Column(Integer)
    size = Column(String)
    temperament = Column(String)
    status = Column(String)

    adoptions = relationship("AdoptionModel", back_populates="animal")