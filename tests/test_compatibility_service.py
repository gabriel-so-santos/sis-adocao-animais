import pytest
from domain.animals.cat import Cat
from domain.animals.dog import Dog
from domain.people.adopter import Adopter, HousingType
from domain.animals.animal import Size, Gender, AnimalStatus, Species
from services.compatibility_service import CompatibilityService
from datetime import datetime

@pytest.fixture
def service():
    return CompatibilityService()

@pytest.fixture
def adopter():
    return Adopter(
        name="Alice",
        age=30,
        housing_type=HousingType.HOUSE,
        usable_area=50,
        has_pet_experience=True,
        has_children_at_home=False,
        has_other_animals=True
    )

@pytest.fixture
def dog():
    return Dog(
        species=Species.DOG,
        breed="vira-lata",
        name="Rex",
        gender=Gender.MALE,
        age_months=12,
        size=Size.MEDIUM,
        temperament=["Brincalhão"],
        status=AnimalStatus.AVAILABLE,
        needs_walk=True
    )

@pytest.fixture
def cat():
    return Cat(
        species=Species.CAT,
        breed="Siamês",
        name="Luna",
        gender=Gender.FEMALE,
        age_months=8,
        size=Size.SMALL,
        temperament=["Calma"],
        status=AnimalStatus.AVAILABLE,
        is_hypoallergenic=False
    )

# ---------------------- TESTE DE CÁLCULO GERAL ----------------------

def test_calculate_rate_returns_float(service, dog, adopter):
    rate = service.calculate_rate(dog, adopter)
    assert isinstance(rate, float)
    assert 0 <= rate <= 100

def test_calculate_rate_for_cat(service, cat, adopter):
    rate = service.calculate_rate(cat, adopter)
    assert isinstance(rate, float)
    assert 0 <= rate <= 100

# ---------------------- TESTES DE CADA CRITÉRIO ----------------------

def test_score_size_vs_area_above_min(service, dog, adopter):
    adopter.usable_area = 100  # muito maior que mínimo
    score = service._CompatibilityService__score_size_vs_area(dog, adopter)
    assert score > 0

def test_score_size_vs_area_below_min(service, dog, adopter):
    adopter.usable_area = 1  # menor que mínimo
    score = service._CompatibilityService__score_size_vs_area(dog, adopter)
    assert score >= 0

def test_score_size_vs_housing(service, dog, adopter):
    score = service._CompatibilityService__score_size_vs_housing(dog, adopter)
    assert score >= 0

def test_score_pet_age_vs_experience(service, dog, adopter):
    score = service._CompatibilityService__score_pet_age_vs_has_experience(dog, adopter)
    assert score >= 0

def test_score_temperament_vs_children(service, dog, adopter):
    adopter.has_children_at_home = True
    score = service._CompatibilityService__score_temperament_vs_has_children(dog, adopter)
    assert score >= 0

def test_score_adopter_age(service, adopter):
    score = service._CompatibilityService__score_adopter_age(adopter)
    assert score >= 0

def test_score_other_animals(service, adopter):
    score = service._CompatibilityService__score_other_animals(adopter)
    assert score >= 0
