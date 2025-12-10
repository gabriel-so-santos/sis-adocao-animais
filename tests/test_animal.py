import pytest
from domain.animals.animal_status import AnimalStatus
from domain.exeptions import InvalidStatusTransitionError
from domain.animals.animal import Animal, Species, Gender, Size


# ---------------------------------------------------------
# Classe concreta para poder testar Animal (pois é abstrata)
# ---------------------------------------------------------
class FakeAnimal(Animal):
    pass


# ---------------------------------------------------------
# FIXTURE: cria um animal válido para testes
# ---------------------------------------------------------
@pytest.fixture
def animal():
    return FakeAnimal(
        id=1,
        species=Species.CAT,
        breed="siamês",
        name="luna",
        gender=Gender.FEMALE,
        age_months=12,
        size=Size.SMALL,
        temperament=["calma", "brincalhona"],
        status=AnimalStatus.AVAILABLE
    )


# ---------------------------------------------------------
# TESTES DE FORMATAÇÃO
# ---------------------------------------------------------

def test_species_format_female(animal):
    assert animal.species_format() == "Gata"


def test_species_format_male(animal):
    animal.gender = Gender.MALE
    assert animal.species_format() == "Gato"


def test_gender_format(animal):
    assert animal.gender_format() == "Fêmea"


def test_size_format(animal):
    assert animal.size_format() == "Pequeno"


def test_temperament_format(animal):
    assert animal.temperament_format() == "Calma, Brincalhona"


def test_status_format(animal):
    assert animal.status_format() == "Disponível"


# ---------------------------------------------------------
# TESTES DE VALIDAÇÕES DOS SETTERS
# ---------------------------------------------------------

def test_invalid_species():
    with pytest.raises(ValueError):
        FakeAnimal(
            id=1,
            species="CAT",  # inválido
            breed="Siamês",
            name="Luna",
            gender=Gender.FEMALE,
            age_months=12,
            size=Size.SMALL,
            temperament=[],
        )


def test_invalid_breed_value():
    with pytest.raises(ValueError):
        FakeAnimal(
            id=1,
            species=Species.CAT,
            breed="   ",    # inválido
            name="Luna",
            gender=Gender.FEMALE,
            age_months=12,
            size=Size.SMALL,
            temperament=[],
        )

def test_invalid_breed_type():
    with pytest.raises(TypeError):
        FakeAnimal(
            id=1,
            species=Species.CAT,
            breed=123,    # inválido
            name="Luna",
            gender=Gender.FEMALE,
            age_months=12,
            size=Size.SMALL,
            temperament=[],
        )


def test_invalid_name_value():
    with pytest.raises(ValueError):
        FakeAnimal(
            id=1,
            species=Species.CAT,
            breed="Siamês",
            name="",        # inválido
            gender=Gender.FEMALE,
            age_months=12,
            size=Size.SMALL,
            temperament=[],
        )

def test_invalid_name_type():
    with pytest.raises(TypeError):
        FakeAnimal(
            id=1,
            species=Species.CAT,
            breed="Siamês",
            name=123,        # inválido
            gender=Gender.FEMALE,
            age_months=12,
            size=Size.SMALL,
            temperament=[],
        )


def test_invalid_gender():
    with pytest.raises(TypeError):
        FakeAnimal(
            id=1,
            species=Species.CAT,
            breed="Siamês",
            name="Luna",
            gender="FEMALE",  # inválido
            age_months=12,
            size=Size.SMALL,
            temperament=[],
        )


def test_invalid_age_type(animal):
    with pytest.raises(TypeError):
        animal.age_months = "10"


def test_invalid_age_negative(animal):
    with pytest.raises(ValueError):
        animal.age_months = -1


def test_invalid_size():
    with pytest.raises(TypeError):
        FakeAnimal(
            id=1,
            species=Species.CAT,
            breed="Siamês",
            name="Luna",
            gender=Gender.FEMALE,
            age_months=12,
            size="SMALL",
            temperament=[],
        )


def test_invalid_temperament_not_list(animal):
    with pytest.raises(TypeError):
        animal.temperament = "calma"


def test_invalid_temperament_item_not_string(animal):
    with pytest.raises(TypeError):
        animal.temperament = ["ok", 123]


# ---------------------------------------------------------
# TESTES DE TRANSIÇÃO DE STATUS
# ---------------------------------------------------------

def test_valid_status_transition(animal):
    animal.status = AnimalStatus.RESERVED
    assert animal.status == AnimalStatus.RESERVED


def test_invalid_status_transition(animal, monkeypatch):
    # Mocka o método is_valid_transition para forçar transição inválida
    monkeypatch.setattr(
        "domain.animals.animal_status.AnimalStatus.is_valid_transition",
        lambda current, new: False
    )

    with pytest.raises(InvalidStatusTransitionError):
        animal.status = AnimalStatus.ADOPTED