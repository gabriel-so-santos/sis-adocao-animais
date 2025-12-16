from domain.animals.cat import Cat
from domain.animals.dog import Dog
from domain.people.adopter import Adopter
import json

with open("settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)

class CompatibilityService:

    def __init__(self):
        self.weights = settings["compatibility"]["weights"]
        self.scores = settings["compatibility"]["scores"]

    def calculate_rate(self, animal: Cat | Dog, adopter: Adopter) -> float:
        """
        Calcula o índice de compatibilidade entre um animal e um adotante.

        O cálculo é realizado a partir da soma ponderada de diversos critérios,
        cujos pesos e pontuações base são definidos no arquivo settings.json.
        Cada critério gera uma pontuação parcial (0 a 100), multiplicada pelo
        peso correspondente.

        O valor final é limitado ao intervalo de 0 a 100.

        Args:
            animal (Cat | Dog): Animal candidato à adoção.
            adopter (Adopter): Adotante interessado no animal.

        Returns:
            float: Pontuação final de compatibilidade no intervalo de 0 a 100.
        """
        total_score = 0.0

        total_score += self.__score_size_vs_area(animal, adopter)
        total_score += self.__score_size_vs_housing(animal, adopter)
        total_score += self.__score_pet_age_vs_has_experience(animal, adopter)
        total_score += self.__score_temperament_vs_has_children(animal, adopter)
        total_score += self.__score_adopter_age(adopter)
        total_score += self.__score_other_animals(adopter)

        total_score = min(total_score, 100)
        total_score = round(total_score, 2)

        return total_score
    
    # ---------------- SCORE METHODS ----------------
    
    def __score_size_vs_area(self, animal: Cat | Dog, adopter: Adopter) -> float:
        """
        Avalia a compatibilidade entre o porte do animal e a área útil
        disponível na moradia do adotante.
        """
        weight = self.weights["size_vs_area"]
        size_key = animal.size.name

        min_area = settings["policies"]["minimum_area"][size_key]

        if adopter.usable_area >= min_area:
            base_score = self.scores["size_vs_area"][size_key]["above_min"]
        else:
            base_score = self.scores["size_vs_area"][size_key]["bellow_min"]

        return base_score * weight

    def __score_size_vs_housing(self, animal: Cat | Dog, adopter: Adopter) -> float:
        """
        Avalia a compatibilidade entre o porte do animal e o tipo de
        moradia do adotante (casa ou apartamento).
        """
        weight = self.weights["size_vs_housing"]

        size_key = animal.size.name
        housing_key = adopter.housing_type.name

        base_score = self.scores["size_vs_housing"][size_key][housing_key]

        return base_score * weight

    def __score_pet_age_vs_has_experience(self, animal: Cat | Dog, adopter: Adopter) -> float:
        """
        Avalia a relação entre a idade do animal e a experiência prévia
        do adotante com outros pets.
        """
        weight = self.weights["pet_age_vs_has_experience"]

        pet_age_group = animal.age_group()
        experience_key = "has_experience" if adopter.has_pet_experience else "none"

        base_score = self.scores["pet_age_vs_has_experience"][pet_age_group][experience_key]

        return base_score * weight

    def __score_temperament_vs_has_children(self, animal: Cat | Dog, adopter: Adopter) -> float:
        """
        Pontua a compatibilidade entre o temperamento do animal e a presença de crianças na residência.
        A presença de crianças reduz a pontuação para animais ariscos
        """
        weight = self.weights["temperament_vs_has_children"]

        temperament_key = (
            "wary_temperament"
            if animal.has_wary_temperament()
            else "regular_temperament"
        )

        children_key = "has_children" if adopter.has_children_at_home else "none"

        base_score = self.scores["temperament_vs_has_children"][temperament_key][children_key]

        return base_score * weight
    
    def __score_adopter_age(self, adopter: Adopter) -> float:
        """
        Pontua a compatibilidade com base na faixa etária do adotante.
        """
        weight = self.weights["adopter_age"]

        age_group = adopter.age_group()
        base_score = self.scores["adopter_age"][age_group]

        return base_score * weight

    def __score_other_animals(self, adopter: Adopter) -> float:
        """
        Pontua a compatibilidade considerando a presença de outros animais.
        """
        weight = self.weights["other_animals"]

        key = "true" if adopter.has_other_animals else "false"
        base_score = self.scores["has_other_animals"][key]

        return base_score * weight