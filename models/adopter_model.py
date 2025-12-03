from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship
from models.base_model import Base

class AdopterModel(Base):
    __tablename__ = "adopters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    age = Column(Integer)
    housing_type = Column(String)         
    usable_area = Column(Float)
    has_pet_experience = Column(Boolean)
    has_children_at_home = Column(Boolean)
    has_other_animals = Column(Boolean)

    adoptions = relationship("AdoptionModel", back_populates="adopter")