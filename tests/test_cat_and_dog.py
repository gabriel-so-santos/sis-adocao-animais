import pytest
from datetime import datetime

from domain.animals.cat import Cat
from domain.animals.dog import Dog
from domain.animals.animal import Species, Gender, Size, AnimalStatus

# ---------------------------------------------------------
# FIXTURE: CAT VÁLIDO
# ---------------------------------------------------------
@pytest.fixture
def cat():
    return Cat(
        species=Species.CAT,
        breed="siamês",
        name="luna",
        gender=Gender.FEMALE,
        age_months=12,
        size=Size.SMALL,
        temperament=["calma"],
        status=AnimalStatus.AVAILABLE,
        is_hypoallergenic=True,
        id=1,
        timestamp=datetime(2024, 1, 1)
    )


# ---------------------------------------------------------
# TESTES DE INICIALIZAÇÃO
# ---------------------------------------------------------
def test_cat_initialization(cat):
    assert cat.species == Species.CAT
    assert cat.breed == "Siamês"
    assert cat.name == "Luna"
    assert cat.is_hypoallergenic is True


# ---------------------------------------------------------
# TESTES DE MIXIN (Vaccinable)
# ---------------------------------------------------------
def test_cat_is_vaccineable(cat):
    assert hasattr(cat, "is_vaccineable")
    assert cat.is_vaccineable is True


# ---------------------------------------------------------
# TESTES DE VALIDAÇÃO
# ---------------------------------------------------------
def test_cat_invalid_is_hypoallergenic_type(cat):
    with pytest.raises(TypeError):
        cat.is_hypoallergenic = "yes"


# ---------------------------------------------------------
# FIXTURE: DOG VÁLIDO
# ---------------------------------------------------------
@pytest.fixture
def dog():
    return Dog(
        species=Species.DOG,
        breed="vira lata",
        name="rex",
        gender=Gender.MALE,
        age_months=24,
        size=Size.MEDIUM,
        temperament=["brincalhão"],
        status=AnimalStatus.AVAILABLE,
        needs_walk=True,
        id=2,
        timestamp=datetime(2024, 1, 1)
    )


# ---------------------------------------------------------
# TESTES DE INICIALIZAÇÃO
# ---------------------------------------------------------
def test_dog_initialization(dog):
    assert dog.species == Species.DOG
    assert dog.breed == "Vira lata"
    assert dog.name == "Rex"
    assert dog.needs_walk is True


# ---------------------------------------------------------
# TESTES DE MIXINS
# ---------------------------------------------------------
def test_dog_is_vaccineable(dog):
    assert hasattr(dog, "is_vaccineable")
    assert dog.is_vaccineable is True


def test_dog_is_trainable(dog):
    assert hasattr(dog, "is_trainable")
    assert dog.is_trainable is True


# ---------------------------------------------------------
# TESTES DE VALIDAÇÃO
# ---------------------------------------------------------
def test_dog_invalid_needs_walk_type(dog):
    with pytest.raises(TypeError):
        dog.needs_walk = "yes"

