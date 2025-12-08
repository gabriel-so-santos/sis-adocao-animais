from domain.animals.animal import Animal, Species, Gender, Size, AnimalStatus
from domain.mixins.vaccinable_mixin import  VaccinableMixin

class Cat(VaccinableMixin, Animal):
    """Gato com características específicas."""
    html_icon = "fa-solid fa-cat"

    def __init__(self,
        id: int,
        species: Species,
        breed: str,
        name: str,
        gender: Gender,
        age_months: int,
        size: Size,
        temperament: list[str] | None,
        status: AnimalStatus,

        is_hypoallergenic: bool
        ):

        super().__init__(
            id, species, breed, name, gender, age_months, size, temperament, status
        )
        self.is_hypoallergenic = is_hypoallergenic

    def extra_info(self):
        return f"É Hipoalergênico?: {'Sim' if self.is_hypoallergenic else 'Não'}"
    
    def is_hypoallergenic_format(self):
        return 'Sim' if self.is_hypoallergenic else 'Não'

    @property
    def is_hypoallergenic(self) -> bool:
        return self.__is_hypoallergenic
    
    @is_hypoallergenic.setter
    def is_hypoallergenic(self, v: bool) -> None:
        if not isinstance(v, bool):
            raise TypeError("is_hypoallergenic deve ser um booleano.")
        self.__is_hypoallergenic = v

    def __str__(self):
        return (
            f"Nome: {self.name}\n"
            f"Espécie: {self.species_format()}\n"
            f"Raça: {self.breed}\n"
            f"Sexo: {self.gender_format()}\n"
            f"Idade: {self.age_months} meses\n"
            f"Porte: {self.size_format()}\n"
            f"Temperamento: {self.temperament_format()}\n"
            f"Status atual: {self.status_format()}\n"
            f"{self.extra_info()}"
        )