import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

engine = create_engine(f"sqlite:///{DB_PATH}", echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

def init_db():
    """Cria todas as tabelas definidas pelos modelos ORM."""
    from infrastructure.models import(
        adopter_model,
        animal_model,
        event_model
    )
    Base.metadata.create_all(bind=engine)