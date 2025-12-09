from flask import render_template, redirect, url_for, request
from main import app, session
import json

from domain.animals.animal import Species, Gender, Size, AnimalStatus
from repositories.animal_repo import AnimalRepository

from domain.people.adopter import Adopter, HousingType
from repositories.adopter_repo import AdopterRepository

from domain.events.events import EventType, ReservationEvent, AdoptionEvent
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

    if species == Species.CAT:
        from domain.animals.cat import Cat

        animal = Cat(
            id = None,
            species = species,
            breed = request.form["breed"],
            name = request.form["name"],
            gender = Gender[request.form["gender"].upper()],
            age_months = int(request.form["age_months"]),
            size = Size[request.form["size"].upper()],
            temperament = [t.strip() for t in request.form["temperament"].split(",") if t.strip()],
            status = AnimalStatus[request.form["status"].upper()],

            is_hypoallergenic = request.form.get("is_hypoallergenic", "false") == "true"
        )

    else:
        from domain.animals.dog import Dog

        animal = Dog(
            id = None,
            species = species,
            breed = request.form["breed"],
            name = request.form["name"],
            gender = Gender[request.form["gender"].upper()],
            age_months = int(request.form["age_months"]),
            size = Size[request.form["size"].upper()],
            temperament = [t.strip() for t in request.form["temperament"].split(",") if t.strip()],
            status = AnimalStatus[request.form["status"].upper()],
            
            needs_walk = request.form.get("needs_walk", "false") == "true"
        )

    animal_repo.save(animal)
    return redirect(url_for("homepage"))

@app.route("/animals/details/<id>", methods=["GET", "POST"])
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
            name = request.form["name"],
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

@app.route("/adoptions/reservations/new", methods=["GET", "POST"])
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
    animal_id = int(request.form.get("animal_id"))
    adopter_id = int(request.form.get("adopter_id"))

    reservation_event = ReservationEvent(
        id=None,
        animal_id=animal_id,
        adopter_id=adopter_id,
        timestamp=None,
    )
    event_repo.save(reservation_event)

    return redirect(url_for("adoption_reservation_list"))