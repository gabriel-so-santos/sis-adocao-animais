from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from infrastructure.database.db_connection import Base

class EventModel(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    animal_id = Column(Integer, ForeignKey("animals.id"), nullable=False)
    event_type = Column(String, nullable=False)  
    timestamp = Column(DateTime, nullable=False)

    extra_data = Column(JSON, nullable=True)         

    animal = relationship("AnimalModel", back_populates="events")