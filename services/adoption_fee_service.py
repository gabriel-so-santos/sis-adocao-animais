import json
from domain.animals.animal import Animal

with open("settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)


class AdoptionFeeService:
    """
    Serviço responsável por calcular a taxa de adoção de um animal.

    O cálculo é baseado em configurações externas (settings.json),
    considerando valor base, idade do animal, condições especiais
    e limites mínimos e máximos.
    """
    def __init__(self):
        self.settings = settings["policies"]["adoption_fee"]

    def calculate_fee(self, animal: Animal) -> float:
        """
        Calcula a taxa final de adoção para um animal.

        Args:
            animal (Animal): Animal a ser adotado.

        Returns:
            float: Valor final da taxa de adoção.
        """
        fee = self.settings["base_fee"]
        fee += self.__age_adjustment(animal)
        fee = self.__apply_limits(fee)

        return fee

    def __age_adjustment(self, animal: Animal) -> float:
        """Aplica ajuste de taxa conforme a idade do animal."""
        age_group = animal.age_group()
        return self.settings["age_adjustments"][age_group]

    def __apply_limits(self, fee: float) -> float:
        """Garante que a taxa esteja dentro dos limites configurados."""
        min_fee = self.settings["limits"]["minimum_fee"]
        max_fee = self.settings["limits"]["maximum_fee"]
        return max(min_fee, min(fee, max_fee))
