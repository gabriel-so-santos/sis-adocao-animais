from enum import Enum, auto
from domain.people.person import Person
from domain.exeptions import PolicyNotMetError
import json

with open("settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)
    
minimum_age =  settings["policies"]["minimum_adopter_age"]

class HousingType(Enum):
    HOUSE = "HOUSE"
    APARTMENT = "APARTMENT"

class Adopter(Person):
    """Representa um adotante de animais no sistema.
    Contém atributos relevantes para o cálculo de compatibilidade com animais,
    como tipo de moradia, experiência, presença de crianças e outros pets.

    Attributes:
        housing (HousingType): Tipo de moradia do adotante.
        usable_area (float): Área útil do imóvel em m².
        has_pet_experience (bool): Indica se possui experiência prévia com pets.
        has_children_at_home (bool): Indica se há crianças na residência.
        has_other_animals (bool): Indica se já existem outros animais na casa.
    """

    def __init__(
        self,
        id: int,
        name: str,
        age: int,
        housing_type: HousingType,
        usable_area: float,
        has_pet_experience: bool = False,
        has_children_at_home: bool = False,
        has_other_animals: bool = False
    ):
        super().__init__(id=id, name=name, age=age)

        self.housing_type = housing_type
        self.usable_area = usable_area
        self.has_pet_experience = has_pet_experience
        self.has_children_at_home = has_children_at_home
        self.has_other_animals = has_other_animals

    def compatibility_rate(self) -> float:
        """Calcula o score de compatibilidade entre o adotante e um animal.
        ...

        Returns:
            float: Valor entre 0 e 100 representando o nível de compatibilidade.
        """
        pass

    def has_pet_experience_format(self):
        return "Sim" if self.has_pet_experience else "Não"

    def has_children_at_home_format(self):
        return "Sim" if self.has_children_at_home else "Não"

    def has_other_animals_format(self):
        return "Sim" if self.has_other_animals else "Não"

    def housing_type_format(self):
        return {
            "HOUSE": "Casa",
            "APARTMENT": "Apartamento"
        }.get(self.housing_type.name)
        
    # -------------------------- PROPERTIES --------------------------

    # ---- Age ----
    @property
    def age(self) -> int:
        return self.__age

    @age.setter
    def age(self, v: int) -> None:

        if not isinstance(v, int):
            raise TypeError("age deve ser do tipo int.")
        
        if v < minimum_age:
            raise PolicyNotMetError(f"A idade mínima para adotantes é {minimum_age} anos.")
        
        if not (0 <= v <= 128):
            raise ValueError("Idade fora do intervalo permitido.")
        
        self.__age = v

    # ---- Housing Type ----
    @property
    def housing_type(self) -> HousingType: 
        return self.__housing_type
    
    @housing_type.setter
    def housing_type(self, v: HousingType) -> None:
        if not isinstance(v, HousingType):
            raise TypeError("housing_type deve ser item do enum HousingType.")
        self.__housing_type = v

    # ---- Usable Area ----
    @property
    def usable_area(self) -> float:
        return self.__usable_area
    
    @usable_area.setter
    def usable_area(self, v: float) -> None:
        if v <= 0:
            raise ValueError("usable_area deve ser maior que zero.")
        self.__usable_area = v
    
    # ---- Pet Experience ----
    @property
    def has_pet_experience(self) -> bool:
        return self.__has_pet_experience
    
    @has_pet_experience.setter
    def has_pet_experience(self, v: bool) -> None:
        if not isinstance(v, bool):
            raise TypeError("has_pet_experience deve ser um booleano.")
        self.__has_pet_experience = v

    # ---- Children at Home ----
    @property
    def has_children_at_home(self) -> bool:
        return self.__has_children_at_home

    @has_children_at_home.setter
    def has_children_at_home(self, v: bool) -> None:
        if not isinstance(v, bool):
            raise TypeError("has_children_at_home deve ser um booleano.")
        self.__has_children_at_home = v

    # ---- Other Animals ----
    @property
    def has_other_animals(self) -> bool: 
        return self.__has_other_animals
    
    @has_other_animals.setter
    def has_other_animals(self, v: bool) -> None:
        if not isinstance(v, bool):
            raise TypeError("has_other_animals deve ser um booleano.")
        self.__has_other_animals = v