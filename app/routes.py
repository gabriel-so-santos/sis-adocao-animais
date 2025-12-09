from flask import render_template, redirect, url_for, request
from main import app, session
import json
from datetime import datetime

from domain.animals.animal import Species, Gender, Size, AnimalStatus
from repositories.animal_repo import AnimalRepository

from domain.people.adopter import Adopter, HousingType
from repositories.adopter_repo import AdopterRepository

from domain.events.events import EventType, ReservationEvent, AdoptionEvent, VaccineEvent, TrainingEvent
from repositories.event_repo import EventRepository

with open("settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)

@app.route("/")
def homepage():
    return render_template("index.html")

# -------------------------- ANIMALS --------------------------

animal_repo = AnimalRepository(session)

@app.route("/animals", methods=["GET", "POST"])
def animals_list():
    animals_db = animal_repo.list_all()
    animals = list()
    
    for animal_db in animals_db:
        animal = animal_repo.to_domain(animal_db)
        animals.append(animal)

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

    if species == Species.CAT:
        from domain.animals.cat import Cat

        animal = Cat(
            id = None,
            species = species,
            breed = request.form["breed"].strip().capitalize(),
            name = request.form["name"].strip().capitalize(),
            gender = Gender[request.form["gender"].upper()],
            age_months = int(request.form["age_months"]),
            size = Size[request.form["size"].upper()],
            temperament = temperament,
            status = AnimalStatus[request.form["status"].upper()],

            is_hypoallergenic = request.form.get("is_hypoallergenic", "false") == "true"
        )

    else:
        from domain.animals.dog import Dog

        animal = Dog(
            id = None,
            species = species,
            breed = request.form["breed"].strip().capitalize(),
            name = request.form["name"].strip().capitalize(),
            gender = Gender[request.form["gender"].upper()],
            age_months = int(request.form["age_months"]),
            size = Size[request.form["size"].upper()],
            temperament = temperament,
            status = AnimalStatus[request.form["status"].upper()],
            
            needs_walk = request.form.get("needs_walk", "false") == "true"
        )

    animal_repo.save(animal)
    return redirect(url_for("homepage"))

@app.route("/animals/<id>/details", methods=["GET", "POST"])
def animal_details(id):
    animal_db = animal_repo.get_by_id(id)
    animal = animal_repo.to_domain(animal_db)

    return render_template("animal_details.html", animal=animal)

# -------------------------- ADOPTERS --------------------------

adopter_repo = AdopterRepository(session)
min_adopter_age = settings["policies"]["minimum_adopter_age"]

@app.route("/adopters", methods=["GET", "POST"])
def adopters_list():
    adopters_db = adopter_repo.list_all()
    adopters = list()
    
    for adopter_db in adopters_db:
        adopter = adopter_repo.to_domain(adopter_db)
        adopters.append(adopter)

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
    
    else:
        adopter = Adopter(
            id = None,
            name = request.form["name"].strip().capitalize(),
            age = age,
            housing_type = HousingType[request.form["housing_type"].upper()],
            usable_area = float(request.form["usable_area"]),
            has_pet_experience = request.form["has_pet_experience"] == "true",
            has_children_at_home = request.form["has_children_at_home"] == "true",
            has_other_animals = request.form["has_other_animals"] == "true"
        )

        adopter_repo.save(adopter)
        return redirect(url_for("homepage"))

# -------------------------- EVENTS --------------------------

event_repo = EventRepository(session)

#RESERVATION
@app.route("/adoptions/reservations")
def adoption_reservation_list():
    reservations_db = event_repo.list_by_type(EventType.RESERVATION)
    reservations = list()

    for reservation_db in reservations_db:
        reservation = event_repo.to_domain(reservation_db)
        reservations.append(reservation)

    reservations_full = list()
    for r in reservations:
        animal = animal_repo.to_domain(animal_repo.get_by_id(r.animal_id))
        adopter = adopter_repo.to_domain(adopter_repo.get_by_id(r.adopter_id))

        reservations_full.append({
                "id": r.id,
                "date": r.timestamp,
                "animal": animal,
                "adopter": adopter
            })


    return render_template("adoption_reservation_list.html", reservations=reservations_full)

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
        selected_animal_db = animal_repo.get_by_id(animal_id)
        selected_animal = animal_repo.to_domain(selected_animal_db)
    else:
        animals_db = animal_repo.list_all()
        animals = [animal_repo.to_domain(a) for a in animals_db]

    # ADOPTER
    if adopter_id:
        selected_adopter_db = adopter_repo.get_by_id(adopter_id)
        selected_adopter = adopter_repo.to_domain(selected_adopter_db)
    else:
        adopters_db = adopter_repo.list_all()
        adopters = [adopter_repo.to_domain(a) for a in adopters_db]

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

    animal_repo.update_status(id=animal_id, new_status=AnimalStatus.RESERVED)
    reservation= ReservationEvent(
        id=None,
        animal_id=animal_id,
        timestamp=None,
        adopter_id=adopter_id,
    )
    event_repo.save(reservation)

    return redirect(url_for("adoption_reservation_list"))

@app.route("/adoptions/reservations/confirm")
def confirm_adoption():
    id = request.args.get("id")

    reservation_db = event_repo.get_by_id(id)
    reservation = event_repo.to_domain(reservation_db)

    animal_id = reservation.animal_id
    adopter_id = reservation.adopter_id

    saved_reservations = event_repo.list_by_type(
        event_type=EventType.RESERVATION,
        animal_id=animal_id
    )

    for r in saved_reservations:
        event_repo.delete_by_id(r.id)

    animal_repo.update_status(id=animal_id, new_status=AnimalStatus.ADOPTED)
    adoption = AdoptionEvent(
        id=None,
        animal_id=animal_id,
        timestamp=None,
        adopter_id=adopter_id,
        fee=0
    )
    event_repo.save(adoption)

    return redirect(url_for("adoption_reservation_list"))

@app.route("/adoptions/reservations/cancel")
def cancel_reservation():
    id = request.args.get("id")

    event_repo.delete_by_id(id)
    return redirect(url_for("adoption_reservation_list"))

#VACCINE
@app.route("/animals/<animal_id>/vaccine/new")
def vaccine_registration(animal_id):

    animal_db = animal_repo.get_by_id(animal_id)
    animal = animal_repo.to_domain(animal_db)

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

#TRAINING
@app.route("/animals/<animal_id>/training/new")
def training_registration(animal_id):

    animal_db = animal_repo.get_by_id(animal_id)
    animal = animal_repo.to_domain(animal_db)

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