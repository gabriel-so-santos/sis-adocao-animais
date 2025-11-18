from enum import Enum, auto
from person import Person

class HousingType(Enum):
    HOUSE = auto()
    APARTMENT = auto()

class Adopter(Person):
    """Representa um adotante de animais no sistema.
    Contém atributos relevantes para o cálculo de compatibilidade com animais,
    como tipo de moradia, experiência, presença de crianças e outros pets.

    Attributes:
        housing (HousingType): Tipo de moradia do adotante.
        usable_area (float): Área útil do imóvel em m².
        pet_experience (bool): Indica se possui experiência prévia com pets.
        children_at_home (bool): Indica se há crianças na residência.
        other_animals (bool): Indica se já existem outros animais na casa.
    """

    def __init__(
        self,
        name: str,
        age: int,
        housing: HousingType,
        usable_area: float,
        pet_experience: bool = False,
        children_at_home: bool = False,
        other_animals: bool = False,
    ):
        super().__init__(name=name, age=age)
        self.housing = housing
        self.usable_area = usable_area
        self.pet_experience = pet_experience
        self.children_at_home = children_at_home
        self.other_animals = other_animals

    def calculate_compatibility(self) -> float:
        """Calcula o score de compatibilidade entre o adotante e um animal.
        ...

        Returns:
            float: Valor entre 0 e 100 representando o nível de compatibilidade.
        """
        pass