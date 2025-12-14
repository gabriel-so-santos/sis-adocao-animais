from flask import render_template, redirect, url_for, request
from main import app, session
import json
from datetime import datetime

from domain.animals.animal import Species, Gender, Size, AnimalStatus
from infrastructure.repositories.animal_repo import AnimalRepository

from domain.people.adopter import Adopter, HousingType
from infrastructure.repositories.adopter_repo import AdopterRepository

from domain.adoptions.adoption import Adoption
from infrastructure.repositories.adoption_repo import AdoptionRepository

from domain.adoptions.reservation_queue import ReservationQueue
from infrastructure.repositories.reservation_queue_repo import ReservationQueueRepository

from domain.adoptions.adoption_return import AdoptionReturn
from infrastructure.repositories.adoption_return_repo import AdoptionReturnRepository

from domain.events.events import EventType, VaccineEvent, TrainingEvent
from infrastructure.repositories.event_repo import EventRepository

with open("settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)

@app.route("/")
def homepage():
    return render_template("index.html")

# -------------------------- ANIMALS --------------------------

animal_repo = AnimalRepository(session)

@app.route("/animals", methods=["GET", "POST"])
def animals_list():
    animals = animal_repo.list_all()
    return render_template("animals_list.html", animals=animals)

@app.route("/animals/new")
def animal_registration():
    return render_template("animal_registration.html")

@app.route("/animals/save", methods=["GET", "POST"])
def save_animal():

    species = Species[request.form["species"].upper()]

    temperament = list()
    for t in request.form["temperament"].split(","):
        valor = t.strip().capitalize()
        if valor:
            temperament.append(valor)

    shared_args = dict(
        id=None,
        species = species,
        breed = request.form["breed"].strip().capitalize(),
        name = request.form["name"].strip().capitalize(),
        gender = Gender[request.form["gender"].upper()],
        age_months = int(request.form["age_months"]),
        size = Size[request.form["size"].upper()],
        temperament = temperament,
        status = AnimalStatus[request.form["status"].upper()]
    )

    if species == Species.CAT:
        from domain.animals.cat import Cat
        animal = Cat(
            **shared_args,
            is_hypoallergenic = request.form.get("is_hypoallergenic", "false") == "true"
        )
    else:
        from domain.animals.dog import Dog
        animal = Dog(
            **shared_args,
            needs_walk = request.form.get("needs_walk", "false") == "true"
        )

    was_saved = animal_repo.save(animal)

    if not was_saved:
        return render_template(
            "error.html",
            err_msg="Este animal já tem registro cadastrado."
        )
        
    return redirect(url_for("animals_list"))

@app.route("/animals/<id>/details", methods=["GET", "POST"])
def animal_details(id):
    animal = animal_repo.get_by(id=id)
    return render_template("animal_details.html", animal=animal)

@app.route("/animals/<id>/details/change-status/<status>", methods=["GET", "POST"])
def change_animal_status(id, status):
    new_status = AnimalStatus[status.upper()]

    animal_repo.update_status(id, new_status)
    return redirect(url_for("animal_details", id=id))

# -------------------------- ADOPTERS --------------------------

adopter_repo = AdopterRepository(session)
min_adopter_age = settings["policies"]["minimum_adopter_age"]

@app.route("/adopters", methods=["GET", "POST"])
def adopters_list():
    adopters = adopter_repo.list_all()
    return render_template("adopters_list.html", adopters=adopters)

@app.route("/adopters/new")
def adopter_registration():
    return render_template("adopter_registration.html", minimum_age=min_adopter_age)

@app.route("/adopters/save", methods=["GET", "POST"])
def save_adopter():

    age = int(request.form["age"])

    if age < min_adopter_age:
        return render_template(
            "error.html",
            err_msg=f"""
                Você não cumpre as políticas para cadastro de adotantes.
                A idade mínima para adotantes é {min_adopter_age}."""
            )

    if age > 128:
        return render_template(
            "error.html",
            err_msg="Idade fora do limite permitido."
            )
    
    adopter = Adopter(
        id=None,
        timestamp=None,
        name = request.form["name"].strip().capitalize(),
        age = age,
        housing_type = HousingType[request.form["housing_type"].upper()],
        usable_area = float(request.form["usable_area"]),
        has_pet_experience = request.form["has_pet_experience"] == "true",
        has_children_at_home = request.form["has_children_at_home"] == "true",
        has_other_animals = request.form["has_other_animals"] == "true"
    )

    was_saved = adopter_repo.save(adopter)

    if not was_saved:
        return render_template(
            "error.html",
            err_msg="Este adotante já tem registro cadastrado."
        )

    return redirect(url_for("adopters_list"))

# -------------------------- EVENTS --------------------------

event_repo = EventRepository(session)

reservation_q_repo = ReservationQueueRepository(session)

adoption_repo = AdoptionRepository(session)

adoption_return_repo = AdoptionReturnRepository(session)

# RESERVATION
@app.route("/adoptions/reservations")
def adoption_reservation_list():
    reservations = reservation_q_repo.list_all()

    reservation_data = list()
    for r in reservations:
        animal = animal_repo.get_by(id=r.animal_id)
        adopter = adopter_repo.get_by(id=r.adopter_id)

        reservation_data.append({
                "id": r.id,
                "date": r.timestamp,
                "animal": animal,
                "adopter": adopter
            })

    return render_template("adoption_reservation_list.html", reservations=reservation_data)

@app.route("/adoptions/reservations/new")
def adoption_reservation():
    animal_id = request.args.get("animal_id")
    adopter_id = request.args.get("adopter_id")

    animals = None
    adopters = None
    selected_animal = None
    selected_adopter = None

    # ANIMAL
    if animal_id:
        selected_animal = animal_repo.get_by(animal_id)
    else:
        animals = animal_repo.list_reservable_animals()
        
    # ADOPTER
    if adopter_id:
        selected_adopter = adopter_repo.get_by(adopter_id)
    else:
        adopters = adopter_repo.list_all()
    
    return render_template(
        "adoption_reservation.html",
        animals=animals,
        adopters=adopters,
        selected_animal=selected_animal,
        selected_adopter=selected_adopter,
    )

@app.route("/adoptions/reservations/save", methods=["GET", "POST"])
def save_adoption_reservation():
    animal_id = int(request.form["animal_id"])
    adopter_id = int(request.form["adopter_id"])

    reservation = ReservationQueue(
        animal_id=animal_id,
        adopter_id=adopter_id,
        compatibility_rate=50,
    )

    was_saved = reservation_q_repo.save(reservation)

    if not was_saved:
        return render_template(
            "error.html",
            err_msg="Esta reserva já foi cadastrada."
        )

    animal_repo.update_status(
        id=animal_id,
        new_status=AnimalStatus.RESERVED
    )
    
    return redirect(url_for("adoption_reservation_list"))

# ADOPTION
@app.route("/adoptions/reservations/confirm")
def confirm_adoption():
    reservation_id = request.args.get("id")

    reservation = reservation_q_repo.get_by(id=reservation_id)
    animal_id = reservation.animal_id
    adopter_id = reservation.adopter_id

    reservation_q_repo.clear_queue(animal_id=animal_id)

    animal_repo.update_status(
        id=animal_id,
        new_status=AnimalStatus.ADOPTED
    )

    adoption = Adoption(
        animal_id=animal_id,
        adopter_id=adopter_id,
        fee=0,
    )
    adoption_repo.save(adoption)

    return redirect(url_for("adoption_reservation_list"))

@app.route("/adoptions/reservations/cancel")
def cancel_reservation():
    reservation_id = request.args.get("id")
    reservation_q_repo.delete_by(id=reservation_id)

    return redirect(url_for("adoption_reservation_list"))

@app.route("/adoptions/returns/new")
def adoption_return_registration():
    animal_id = int(request.args.get("animal_id"))
    animal = animal_repo.get_by(id=animal_id)

    return render_template("return_registration.html", animal=animal)

@app.route("/adoptions/returns/save", methods=["GET", "POST"])
def save_adoption_return():
    print(request.form)
    animal_id = int(request.form["animal_id"])

    adoption = adoption_repo.get_by_animal_id(animal_id)

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

    animal = animal_repo.get_by(animal_id)

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

    animal = animal_repo.get_by(animal_id)

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