import pytest
from datetime import datetime

from domain.adoptions.adoption import Adoption

# ---------------------------------------------------------
# FIXTURE: ADOÇÃO VÁLIDA
# ---------------------------------------------------------
@pytest.fixture
def adoption():
    return Adoption(
        animal_id=1,
        adopter_id=2,
        fee=150.0,
        id=10,
        timestamp=datetime(2024, 1, 1)
    )

# ---------------------------------------------------------
# TESTES DE INICIALIZAÇÃO
# ---------------------------------------------------------
def test_adoption_initialization(adoption):
    assert adoption.id == 10
    assert adoption.animal_id == 1
    assert adoption.adopter_id == 2
    assert adoption.fee == 150.0
    assert isinstance(adoption.timestamp, datetime)


# ---------------------------------------------------------
# TESTES ANIMAL ID
# ---------------------------------------------------------
def test_invalid_animal_id_type():
    with pytest.raises(TypeError):
        Adoption(
            animal_id="1",
            adopter_id=1,
            fee=100
        )


def test_invalid_animal_id_value():
    with pytest.raises(ValueError):
        Adoption(
            animal_id=0,
            adopter_id=1,
            fee=100
        )


# ---------------------------------------------------------
# TESTES ADOPTER ID
# ---------------------------------------------------------
def test_invalid_adopter_id_type():
    with pytest.raises(TypeError):
        Adoption(
            animal_id=1,
            adopter_id="2",
            fee=100
        )


def test_invalid_adopter_id_value():
    with pytest.raises(ValueError):
        Adoption(
            animal_id=1,
            adopter_id=0,
            fee=100
        )

# ---------------------------------------------------------
# TESTES FEE
# ---------------------------------------------------------
def test_invalid_fee_type():
    with pytest.raises(TypeError):
        Adoption(
            animal_id=1,
            adopter_id=2,
            fee="gratis"
        )


def test_invalid_fee_negative():
    with pytest.raises(ValueError):
        Adoption(
            animal_id=1,
            adopter_id=2,
            fee=-10
        )


def test_valid_fee_int():
    adoption = Adoption(
        animal_id=1,
        adopter_id=2,
        fee=50
    )
    assert adoption.fee == 50.0

# ---------------------------------------------------------
# TESTES DE PROPRIEDADES IMUTÁVEIS
# ---------------------------------------------------------
def test_adoption_id_is_read_only(adoption):
    with pytest.raises(AttributeError):
        adoption.id = 20


def test_adoption_timestamp_is_read_only(adoption):
    with pytest.raises(AttributeError):
        adoption.timestamp = datetime.now()
