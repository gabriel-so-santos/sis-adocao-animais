import pytest
from datetime import datetime
from domain.animals.animal import Animal
from domain.enums.animal_enums import Species, Gender, Size
from domain.enums.animal_status import AnimalStatus
from domain.exceptions import InvalidStatusTransitionError


# ---------------------------------------------------------
# Classe inválida (não implementa método abstrato corretamente)
# ---------------------------------------------------------
class InvalidAnimal(Animal):
    pass


def test_animal_without_extra_info_cannot_be_instantiated():
    with pytest.raises(TypeError):
        InvalidAnimal(
            species=Species.CAT,
            breed="Siamês",
            name="Luna",
            gender=Gender.FEMALE,
            age_months=10,
            size=Size.SMALL,
            temperament=[],
            status=AnimalStatus.AVAILABLE,
        )


# ---------------------------------------------------------
# Classe válida para testes
# ---------------------------------------------------------
class FakeAnimal(Animal):
    def extra_info(self):
        return "ok"


# ---------------------------------------------------------
# FIXTURE
# ---------------------------------------------------------
@pytest.fixture
def animal(monkeypatch):
    monkeypatch.setattr(
        "domain.animals.animal.settings",
        {"policies": {"wary_animal_temperaments": ["Medroso", "Agressivo"]}}
    )

    return FakeAnimal(
        species=Species.DOG,
        breed="vira lata",
        name="rex",
        gender=Gender.MALE,
        age_months=5,
        size=Size.MEDIUM,
        temperament=[" medroso ", " brincalhão ", ""],
        status=AnimalStatus.AVAILABLE,
        id=1,
        timestamp=datetime(2024, 1, 1)
    )


# ---------------------------------------------------------
# TESTES DE INICIALIZAÇÃO
# ---------------------------------------------------------
def test_animal_initialization(animal):
    assert animal.id == 1
    assert animal.species == Species.DOG
    assert animal.breed == "Vira lata"
    assert animal.name == "Rex"
    assert animal.age_months == 5
    assert animal.temperament == ["Medroso", "Brincalhão"]


# ---------------------------------------------------------
# TESTES DE MÉTODOS DE NEGÓCIO
# ---------------------------------------------------------
def test_animal_str(animal):
    assert str(animal) == "Rex, Cachorro Vira lata"


def test_animal_timestamp(animal):
    assert isinstance(animal.timestamp, datetime)


def test_animal_age_group_young(animal):
    assert animal.age_group() == "young_pet"


def test_animal_age_group_adult(animal):
    animal.age_months = 24
    assert animal.age_group() == "adult_pet"


def test_animal_age_group_senior(animal):
    animal.age_months = 120
    assert animal.age_group() == "senior_pet"


def test_has_wary_temperament_true(animal):
    assert animal.has_wary_temperament() is True


def test_has_wary_temperament_false(animal):
    animal.temperament = ["Calmo"]
    assert animal.has_wary_temperament() is False


# ---------------------------------------------------------
# TESTES DE STATUS
# ---------------------------------------------------------
def test_valid_status_transition(animal):
    animal.status = AnimalStatus.RESERVED
    assert animal.status == AnimalStatus.RESERVED


def test_invalid_status_transition(monkeypatch, animal):
    monkeypatch.setattr(
        "domain.enums.animal_status.AnimalStatus.is_valid_transition",
        lambda current, new: False
    )

    with pytest.raises(InvalidStatusTransitionError):
        animal.status = AnimalStatus.ADOPTED
