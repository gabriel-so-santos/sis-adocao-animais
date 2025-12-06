from flask import render_template, redirect, url_for, request
from main import app, session

from domain.animals.animal import Animal, Species, Gender, Size, AnimalStatus
from repositories.animal_repo import AnimalRepository

from domain.people.adopter import Adopter, HousingType
from repositories.adopter_repo import AdopterRepository

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
            id=None,
            species=species,
            breed=request.form["breed"],
            name=request.form["name"],
            gender=Gender[request.form["gender"].upper()],
            age_months=int(request.form["age_months"]),
            size=Size[request.form["size"].upper()],
            temperament=[t.strip() for t in request.form["temperament"].split(",") if t.strip()],
            status=AnimalStatus[request.form["status"].upper()],
            #independence=True 
        )

    else:
        from domain.animals.dog import Dog
        
        animal = Dog(
            id=None,
            species=species,
            breed=request.form["breed"],
            name=request.form["name"],
            gender=Gender[request.form["gender"].upper()],
            age_months=int(request.form["age_months"]),
            size=Size[request.form["size"].upper()],
            temperament=[t.strip() for t in request.form["temperament"].split(",") if t.strip()],
            status=AnimalStatus[request.form["status"].upper()],
            #needs_walk=True  
        )

    animal_repo.save(animal)
    return redirect(url_for("homepage"))

# -------------------------- ADOPTERS --------------------------

adopter_repo = AdopterRepository(session)

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
    return render_template("adopter_registration.html")

@app.route("/adopters/save", methods=["GET", "POST"])
def save_adopter():

    adopter = Adopter(
        id = None,
        name = request.form["name"],
        age = int(request.form["age"]),
        housing_type = HousingType[request.form["housing_type"].upper()],
        usable_area = int(request.form["usable_area"]),
        has_pet_experience = request.form["has_pet_experience"] == "true",
        has_children_at_home = request.form["has_children_at_home"] == "true",
        has_other_animals = request.form["has_other_animals"] == "true"
    )

    adopter_repo.save(adopter)
    return redirect(url_for("homepage"))