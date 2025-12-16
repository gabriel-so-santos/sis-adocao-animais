import json
from flask import render_template, redirect, url_for, request
from main import(
    app,
    animal_service,
    adopter_service,
    reservation_service,
    adoption_service,
    timeline_service
)

with open("settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)

minimum_age =  settings["policies"]["minimum_adopter_age"]

@app.route("/")
def homepage():
    return render_template("index.html")

# -------------------------- ANIMALS --------------------------
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

# VACCINE
@app.route("/animals/<int:animal_id>/vaccine/new")
def vaccine_registration(animal_id):
    animal = animal_service.prepare_vaccine_form(animal_id)
    return render_template(
        "vaccine_registration.html",
        animal=animal
    )

@app.route("/animals/<int:animal_id>/vaccine/save", methods=["POST"])
def save_vaccine(animal_id):
    animal_service.register_vaccine(
        animal_id=animal_id,
        form_data=request.form
    )
    return redirect(url_for("animal_details", id=animal_id))

# TRAINING
@app.route("/animals/<int:animal_id>/training/new")
def training_registration(animal_id):
    animal = animal_service.prepare_training_form(animal_id)
    return render_template(
        "training_registration.html",
        animal=animal
    )

@app.route("/animals/<int:animal_id>/training/save", methods=["POST"])
def save_training(animal_id):
    animal_service.register_training(
        animal_id=animal_id,
        form_data=request.form
    )
    return redirect(url_for("animal_details", id=animal_id))

# TIMELINE
@app.route("/animals/<animal_id>/details/timeline")
def animal_timeline(animal_id):
    animal = animal_service.get_animal(animal_id)

    events = timeline_service.build_animal_timeline(animal_id=animal_id)

    return render_template(
        "animal_timeline.html",
        animal=animal,
        events=events
    )

# -------------------------- ADOPTERS --------------------------
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

# -------------------------- RESERVATION --------------------------
@app.route("/reservations")
def adoption_reservation_list():
    queues = reservation_service.list_reservations()
    return render_template(
        "adoption_reservation_list.html",
        finished_queues=queues["finished"],
        ongoing_queues=queues["ongoing"]
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
    reservation_service.confirm_adoption(
        reservation_id=int(request.args.get("id"))
    )
    return redirect(url_for("adoption_reservation_list"))

@app.route("/reservations/cancel")
def cancel_reservation():
    reservation_service.cancel_reservation(
        reservation_id=int(request.args.get("id"))
    )
    return redirect(url_for("adoption_reservation_list"))

# -------------------------- ADOPTION --------------------------
@app.route("/adoptions")
def adoptions_list():
    data = adoption_service.list_adoptions()

    return render_template(
        "adoptions_list.html",
        adoptions=data["active"],
        adoption_returns=data["returned"]
    )

@app.route("/adoptions/returns/new")
def adoption_return_registration():
    animal = adoption_service.prepare_return_form(
        animal_id=int(request.args.get("animal_id"))
    )
    return render_template(
        "return_registration.html",
        animal=animal
    )

@app.route("/adoptions/returns/save", methods=["POST"])
def save_adoption_return():
    adoption_service.register_return(
        animal_id=int(request.form["animal_id"]),
        reason=request.form["reason"]
    )
    return redirect(
        url_for(
            "animal_details",
            id=int(request.form["animal_id"])
        )
    )