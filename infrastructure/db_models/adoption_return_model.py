from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from sqlalchemy.orm import relationship
from infrastructure.database.db_connection import Base

class AdoptionReturnModel(Base):
    __tablename__ = "adoption_returns"

    adoption_id = Column(Integer, ForeignKey("adoptions.id", ondelete="CASCADE"), primary_key=True)
    reason = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    # -------------------------- RELATIONSHIPS --------------------------

    adoption = relationship("AdoptionModel", back_populates="adoption_return", uselist=False)