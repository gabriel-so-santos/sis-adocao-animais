import pytest
from datetime import datetime
from domain.people.adopter import Adopter
from domain.enums.adopter_enums import HousingType
from domain.exceptions import PolicyNotMetError


# ---------------------------------------------------------
# MOCK GLOBAL DE POLÍTICA
# ---------------------------------------------------------
@pytest.fixture(autouse=True)
def mock_minimum_age(monkeypatch):
    monkeypatch.setattr(
        "domain.people.adopter.minimum_age",
        18
    )


# ---------------------------------------------------------
# FIXTURE
# ---------------------------------------------------------
@pytest.fixture
def adopter():
    return Adopter(
        name="Carlos",
        age=30,
        housing_type=HousingType.HOUSE,
        usable_area=60,
        has_pet_experience=True,
        has_children_at_home=False,
        has_other_animals=False,
        timestamp=datetime(2024, 1, 1)
    )


# ---------------------------------------------------------
# TESTES DE INICIALIZAÇÃO
# ---------------------------------------------------------
def test_adopter_initialization(adopter):
    assert adopter.name == "Carlos"
    assert adopter.age == 30
    assert adopter.housing_type == HousingType.HOUSE


def test_adopter_timestamp(adopter):
    assert isinstance(adopter.timestamp, datetime)


# ---------------------------------------------------------
# TESTES DE AGE
# ---------------------------------------------------------
def test_adopter_under_minimum_age():
    with pytest.raises(PolicyNotMetError):
        Adopter(
            name="Pedro",
            age=16,
            housing_type=HousingType.HOUSE,
            usable_area=50,
            has_pet_experience=False,
            has_children_at_home=False,
            has_other_animals=False
        )


def test_adopter_invalid_age_type(adopter):
    with pytest.raises(TypeError):
        adopter.age = "30"


def test_adopter_age_group_young():
    adopter = Adopter(
        name="João",
        age=18,
        housing_type=HousingType.APARTMENT,
        usable_area=40,
        has_pet_experience=False,
        has_children_at_home=False,
        has_other_animals=False
    )
    

def test_adopter_age_group_adult(adopter):
    assert adopter.age_group() == "adult"


def test_adopter_age_group_senior(adopter):
    adopter.age = 70
    assert adopter.age_group() == "senior"


# ---------------------------------------------------------
# TESTES DE VALIDAÇÃO
# ---------------------------------------------------------
def test_invalid_housing_type():
    with pytest.raises(TypeError):
        Adopter(
            name="Ana",
            age=30,
            housing_type="HOUSE",
            usable_area=40,
            has_pet_experience=False,
            has_children_at_home=False,
            has_other_animals=False
        )


def test_invalid_usable_area(adopter):
    with pytest.raises(ValueError):
        adopter.usable_area = 0


@pytest.mark.parametrize("attr", [
    "has_pet_experience",
    "has_children_at_home",
    "has_other_animals"
])
def test_invalid_boolean_fields(adopter, attr):
    with pytest.raises(TypeError):
        setattr(adopter, attr, "true")
