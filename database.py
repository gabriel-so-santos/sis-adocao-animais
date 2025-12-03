from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base_model import Base

engine = create_engine("sqlite:///data/database.db", echo=False)

SessionLocal = sessionmaker(bind=engine)

def init_db():
    """Cria todas as tabelas definidas pelos modelos ORM."""
    from models.animal_model import AnimalModel  
    
    Base.metadata.create_all(bind=engine)