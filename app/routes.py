from flask import render_template, redirect, url_for, request
from main import app, session

from domain.animals.animal import Animal, Species, Gender, Size, AnimalStatus
from repositories.animal_repo import AnimalRepository

@app.route("/")
def homepage():
    return render_template("index.html")

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

    animal = Animal(
        id = None,
        species = Species[request.form["species"].upper()],
        breed = request.form["breed"],
        name = request.form["name"],
        gender = Gender[request.form["gender"].upper()],
        age_months = int(request.form["age_months"]),
        size = Size[request.form["size"].upper()],
        # Converte os valores recebibos em lista semparando-os por vígula
        temperament = [t.strip() for t in request.form["temperament"].split(",") if t.strip()],
        status = AnimalStatus[request.form["status"].upper()]
    )

    animal_repo.save(animal)
    return redirect(url_for("homepage"))