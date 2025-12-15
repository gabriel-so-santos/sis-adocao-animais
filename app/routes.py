from flask import render_template, redirect, url_for, request
from main import app, session
from datetime import datetime

from domain.animals.animal import Species, Gender, Size, AnimalStatus
from infrastructure.repositories.animal_repo import AnimalRepository

from domain.people.adopter import Adopter, HousingType, minimum_age
from infrastructure.repositories.adopter_repo import AdopterRepository

from domain.adoptions.adoption import Adoption
from infrastructure.repositories.adoption_repo import AdoptionRepository

from domain.adoptions.reservation_queue import ReservationQueue
from infrastructure.repositories.reservation_queue_repo import ReservationQueueRepository

from domain.adoptions.adoption_return import AdoptionReturn
from infrastructure.repositories.adoption_return_repo import AdoptionReturnRepository

from domain.events.animal_events import VaccineEvent, TrainingEvent, QuarentineEvent
from infrastructure.repositories.event_repo import EventRepository

from services.timeline_service import TimelineService
from services.animal_services import AnimalService
from services.adopter_service import AdopterService
from services.reservation_service import ReservationService

@app.route("/")
def homepage():
    return render_template("index.html")

# -------------------------- ANIMALS --------------------------

animal_repo = AnimalRepository(session)
event_repo = EventRepository(session)

animal_service = AnimalService(
    animal_repo=animal_repo,
    event_repo=event_repo
)

@app.route("/animals", methods=["GET"])
def animals_list():
    animals = animal_service.list_animals()
    return render_template("animals_list.html", animals=animals)

@app.route("/animals/new")
def animal_registration():
    return render_template("animal_registration.html")

@app.route("/animals/save", methods=["POST"])
def save_animal():
    was_saved = animal_service.create_animal(form_data=request.form)

    if not was_saved:
        return render_template(
            "error.html",
            err_msg="Este animal já tem registro cadastrado."
        )

    return redirect(url_for("animals_list"))

@app.route("/animals/<int:id>/details")
def animal_details(id):
    animal = animal_service.get_animal(id)
    return render_template("animal_details.html", animal=animal)

@app.route("/animals/<int:id>/details/change-status/<string:status>")
def change_animal_status(id, status):
    animal_service.change_status(id, status)
    return redirect(url_for("animal_details", id=id))

@app.route("/animals/<animal_id>/details/timeline")
def animal_timeline(animal_id):
    animal = animal_service.get_animal(animal_id)

    timeline = TimelineService(
        adoption_repo=adoption_repo,
        adoption_return_repo=adoption_return_repo,
        event_repo=event_repo,
        adopter_repo=adopter_repo
    )
    events = timeline.build_animal_timeline(animal_id=animal_id)

    return render_template(
        "animal_timeline.html",
        animal=animal,
        events=events
    )

# -------------------------- ADOPTERS --------------------------

adopter_repo = AdopterRepository(session)

adopter_service = AdopterService(
    adopter_repo=adopter_repo,
)

@app.route("/adopters", methods=["GET"])
def adopters_list():
    adopters = adopter_service.list_adopters()
    return render_template("adopters_list.html", adopters=adopters)

@app.route("/adopters/new")
def adopter_registration():
    return render_template(
        "adopter_registration.html",
        minimum_age=minimum_age
    )

@app.route("/adopters/save", methods=["POST"])
def save_adopter():
    try:
        adopter_service.register_adopter(request.form)
        return redirect(url_for("adopters_list"))

    except ValueError as e:
        return render_template(
            "error.html",
            err_msg=str(e)
        )

# -------------------------- EVENTS --------------------------


reservation_q_repo = ReservationQueueRepository(session)

adoption_repo = AdoptionRepository(session)

adoption_return_repo = AdoptionReturnRepository(session)

reservation_service = ReservationService(
    reservation_repo=reservation_q_repo,
    animal_repo=animal_repo,
    adopter_repo=adopter_repo,
    adoption_repo=adoption_repo
)

# RESERVATION
@app.route("/reservations")
def adoption_reservation_list():
    reservations = reservation_service.list_reservations()
    return render_template(
        "adoption_reservation_list.html",
        reservations=reservations
    )

@app.route("/reservations/new")
def adoption_reservation():
    id_args = reservation_service.prepare_reservation_form(
        animal_id=request.args.get("animal_id"),
        adopter_id=request.args.get("adopter_id")
    )

    return render_template(
        "adoption_reservation.html",
        **id_args
    )

@app.route("/reservations/save", methods=["POST"])
def save_adoption_reservation():
    try:
        reservation_service.create_reservation(
            animal_id=int(request.form["animal_id"]),
            adopter_id=int(request.form["adopter_id"])
        )
        return redirect(url_for("adoption_reservation_list"))

    except ValueError as e:
        return render_template(
            "error.html",
            err_msg=str(e)
        )

@app.route("/reservations/confirm")
def confirm_adoption():
    reservation_service.confirm_reservation(
        reservation_id=int(request.args.get("id"))
    )
    return redirect(url_for("adoption_reservation_list"))

@app.route("/reservations/cancel")
def cancel_reservation():
    reservation_service.cancel_reservation(
        reservation_id=int(request.args.get("id"))
    )
    return redirect(url_for("adoption_reservation_list"))

#ADOPTION
@app.route("/adoptions")
def adoptions_list():
    adoptions = adoption_repo.list_all()

    adoption_data = list()
    return_data = list()

    for a in adoptions:
        animal = animal_repo.get_by_id(id=a.animal_id)
        adopter = adopter_repo.get_by_id(id=a.adopter_id)

        is_active = not adoption_return_repo.has_returned_adoption(a.id)


        if is_active:
            adoption_data.append({
                    "id": a.id,
                    "timestamp": a.timestamp,
                    "fee": a.fee,
                    "animal": animal,
                    "adopter": adopter,
            })
        else:
            return_data.append({
                    "id": a.id,
                    "adoption_timestamp": a.timestamp,
                    "return_timestamp": adoption_return_repo.get_timestamp(adoption_id=a.id),
                    "fee": a.fee,
                    "animal": animal,
                    "adopter": adopter,
            })
        
    return render_template("adoptions_list.html", adoptions=adoption_data, adoption_returns=return_data)

@app.route("/adoptions/returns/new")
def adoption_return_registration():
    animal_id = int(request.args.get("animal_id"))
    animal = animal_repo.get_by_id(id=animal_id)

    return render_template("return_registration.html", animal=animal)

@app.route("/adoptions/returns/save", methods=["GET", "POST"])
def save_adoption_return():
    animal_id = int(request.form["animal_id"])

    adoption = adoption_repo.get_latest_by_animal(animal_id)

    adoption_return = AdoptionReturn(
        adoption_id=adoption.id,
        reason=request.form["reason"]
    )
    adoption_return_repo.save(adoption_return)

    animal_repo.update_status(id=animal_id, new_status=AnimalStatus.RETURNED)

    return redirect(url_for("animal_details", id=animal_id))

# VACCINE
@app.route("/animals/<animal_id>/vaccine/new")
def vaccine_registration(animal_id):

    animal = animal_repo.get_by_id(animal_id)

    return render_template("vaccine_registration.html", animal=animal)

@app.route("/animals/<animal_id>/vaccine/save", methods=["POST"])
def save_vaccine(animal_id):

    date_str = request.form["vaccine_date"]
    date = datetime.strptime(date_str, "%Y-%m-%d")

    vaccine = VaccineEvent(
        id=None,
        animal_id=animal_id,
        timestamp=date,
        vaccine_name=request.form["vaccine_name"].strip(),
        veterinarian=request.form.get("veterinarian", None).strip().capitalize()
    )
    event_repo.save(vaccine)

    return redirect(url_for("animal_details", id=animal_id))

# TRAINING
@app.route("/animals/<animal_id>/training/new")
def training_registration(animal_id):

    animal = animal_repo.get_by_id(animal_id)

    return render_template("training_registration.html", animal=animal)

@app.route("/animals/<animal_id>/training/save", methods=["POST"])
def save_training(animal_id):

    date_str = request.form["training_date"]
    date = datetime.strptime(date_str, "%Y-%m-%d")

    training = TrainingEvent(
        id=None,
        animal_id=animal_id,
        timestamp=date,
        duration_min= int(request.form.get("duration_min") or 0),
        training_type=request.form["training_type"],
        trainer=request.form["trainer"].strip().capitalize(),
        notes=request.form["notes"]
    )
    event_repo.save(training)

    return redirect(url_for("animal_details", id=animal_id))