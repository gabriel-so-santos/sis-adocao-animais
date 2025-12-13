from sqlalchemy import(
    UniqueConstraint, Column, Integer, String, ForeignKey, DateTime, JSON
)
from sqlalchemy.orm import relationship
from infrastructure.database.db_connection import Base

class EventModel(Base):
    __tablename__ = "events"

    __table_args__ = (
        UniqueConstraint(
            "animal_id", "event_type", "timestamp"
        ),  # Single-element tuple required by SQLAlchemy
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    animal_id = Column(Integer, ForeignKey("animals.id"), nullable=False)
    event_type = Column(String, nullable=False)  
    timestamp = Column(DateTime, nullable=False)

    extra_data = Column(JSON, nullable=True, default={})    

    # -------------------------- RELATIONSHIPS --------------------------     

    animal = relationship("AnimalModel", back_populates="events")