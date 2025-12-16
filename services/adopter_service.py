from domain.people.adopter import Adopter, minimum_age
from domain.enums.adopter_enums import HousingType

class AdopterService:

    MAX_AGE = 128

    def __init__(self, adopter_repo):
        self.adopter_repo = adopter_repo

    def list_adopters(self):
        return self.adopter_repo.list_all()

    def register_adopter(self, form_data):
        age = int(form_data["age"])

        if age < minimum_age:
            raise ValueError(
                f"""
                Você não cumpre as políticas para cadastro de adotantes.
                A idade mínima para adotantes é {self.minimum_age}.
                """
            )

        if age > self.MAX_AGE:
            raise ValueError("Idade fora do limite permitido.")

        adopter = Adopter(
            name=form_data["name"].strip().capitalize(),
            age=age,
            housing_type=HousingType[form_data["housing_type"].upper()],
            usable_area=float(form_data["usable_area"]),
            has_pet_experience=form_data["has_pet_experience"] == "true",
            has_children_at_home=form_data["has_children_at_home"] == "true",
            has_other_animals=form_data["has_other_animals"] == "true"
        )

        was_saved = self.adopter_repo.save(adopter)

        if not was_saved:
            raise ValueError("Este adotante já tem registro cadastrado.")

        return adopter