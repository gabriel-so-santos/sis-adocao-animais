import pytest
from domain.people.adopter import Adopter, HousingType, minimum_age
from domain.exeptions import PolicyNotMetError


# ---------------------------------------------------------
# FIXTURE: mocka o valor da política de idade mínima
# ---------------------------------------------------------
@pytest.fixture(autouse=True)
def mock_settings(monkeypatch):
    monkeypatch.setattr(
        "domain.people.adopter.settings",
        {"policies": {"minimum_adopter_age": 18}}
    )


# ---------------------------------------------------------
# FIXTURE: cria um adotante válido
# ---------------------------------------------------------
@pytest.fixture
def adopter():
    return Adopter(
        id=1,
        name="Carlos",
        age=25,
        housing_type=HousingType.HOUSE,
        usable_area=50.0,
        has_pet_experience=True,
        has_children_at_home=False,
        has_other_animals=True
    )


# ---------------------------------------------------------
# TESTES DE INICIALIZAÇÃO
# ---------------------------------------------------------

def test_adopter_initialization(adopter):
    assert adopter.id == 1
    assert adopter.name == "Carlos"
    assert adopter.age == 25
    assert adopter.housing_type == HousingType.HOUSE
    assert adopter.usable_area == 50.0
    assert adopter.has_pet_experience is True
    assert adopter.has_children_at_home is False
    assert adopter.has_other_animals is True


# ---------------------------------------------------------
# TESTES DO SETTER DE IDADE (AGE)
# ---------------------------------------------------------

def test_underage_adopter_not_allowed():
    """Menores que a idade mínima devem falhar."""
    with pytest.raises(PolicyNotMetError):
        Adopter(
            id=1,
            name="João",
            age=minimum_age-1,  # menor que a política
            housing_type=HousingType.HOUSE,
            usable_area=40,
        )


def test_invalid_age_type(adopter):
    with pytest.raises(TypeError):
        adopter.age = "25"


def test_age_over_upper_limit(adopter):
    with pytest.raises(ValueError):
        adopter.age = 200


def test_valid_age_change(adopter):
    adopter.age = 45
    assert adopter.age == 45


# ---------------------------------------------------------
# TESTES HOUSING TYPE
# ---------------------------------------------------------

def test_invalid_housing_type():
    with pytest.raises(TypeError):
        Adopter(
            id=1,
            name="Ana",
            age=30,
            housing_type="HOUSE",  # inválido
            usable_area=40,
        )


# ---------------------------------------------------------
# TESTES USABLE AREA
# ---------------------------------------------------------

def test_invalid_usable_area_zero(adopter):
    with pytest.raises(ValueError):
        adopter.usable_area = 0


def test_invalid_usable_area_negative(adopter):
    with pytest.raises(ValueError):
        adopter.usable_area = -10


def test_valid_usable_area(adopter):
    adopter.usable_area = 20.5
    assert adopter.usable_area == 20.5


# ---------------------------------------------------------
# TESTES BOOLEANOS
# ---------------------------------------------------------

@pytest.mark.parametrize("attr", [
    "has_pet_experience",
    "has_children_at_home",
    "has_other_animals"
])
def test_invalid_boolean_fields(adopter, attr):
    with pytest.raises(TypeError):
        setattr(adopter, attr, "true")


def test_valid_boolean_fields(adopter):
    adopter.has_children_at_home = True
    assert adopter.has_children_at_home is True


# ---------------------------------------------------------
# TESTES DE FORMATAÇÃO
# ---------------------------------------------------------

def test_format_pet_experience(adopter):
    assert adopter.has_pet_experience_format() == "Sim"


def test_format_children_at_home(adopter):
    assert adopter.has_children_at_home_format() == "Não"


def test_format_other_animals(adopter):
    assert adopter.has_other_animals_format() == "Sim"


def test_format_housing_type_house(adopter):
    assert adopter.housing_type_format() == "Casa"


def test_format_housing_type_apartment(adopter):
    adopter.housing_type = HousingType.APARTMENT
    assert adopter.housing_type_format() == "Apartamento"