from flask import Flask
from infrastructure.database.db_connection import init_db, Session
from infrastructure.repositories import *
from services import *

# -------------------------- DB INIT --------------------------
init_db()
session = Session()

# -------------------------- REPOSITORIES --------------------------
animal_repo = AnimalRepository(session)
adopter_repo = AdopterRepository(session)
reservation_repo = ReservationQueueRepository(session)
adoption_repo = AdoptionRepository(session)
adoption_return_repo = AdoptionReturnRepository(session)
event_repo = EventRepository(session)

# -------------------------- SERVICES --------------------------
animal_service = AnimalService(
    animal_repo=animal_repo,
    event_repo=event_repo
)
adopter_service =  AdopterService(
    adopter_repo=adopter_repo
)
reservation_service = ReservationService(
    animal_repo=animal_repo,
    adopter_repo=adopter_repo,
    reservation_repo=reservation_repo,
    adoption_repo=adoption_repo
)
adoption_service = AdoptionService(
    animal_repo=animal_repo,
    adopter_repo=adopter_repo,
    adoption_repo=adoption_repo,
    adoption_return_repo=adoption_return_repo
)
timeline_service = TimelineService(
    adoption_repo=adoption_repo,
    adoption_return_repo=adoption_return_repo,
    event_repo=event_repo,
    adopter_repo=adopter_repo
)
contract_service = AdoptionContractService(
    adoption_repo=adoption_repo,
    animal_repo=animal_repo,
    adopter_repo=adopter_repo
)

# -------------------------- APP --------------------------
app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static"
)

from app.routes import *

if __name__ == "__main__":
    app.run(debug=True)