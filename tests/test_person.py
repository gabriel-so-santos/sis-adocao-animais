import pytest
from datetime import datetime
from domain.people.person import Person


# ---------------------------------------------------------
# Classe concreta para testar Person (abstrata)
# ---------------------------------------------------------
class FakePerson(Person):
    pass


# ---------------------------------------------------------
# FIXTURE
# ---------------------------------------------------------
@pytest.fixture
def person():
    return FakePerson(
        id=1,
        name="Alice",
        age=30
    )


# ---------------------------------------------------------
# TESTES DE INICIALIZAÇÃO
# ---------------------------------------------------------
def test_person_initialization(person):
    assert person.id == 1
    assert person.name == "Alice"
    assert person.age == 30


# ---------------------------------------------------------
# TESTES DE NAME
# ---------------------------------------------------------
def test_person_invalid_name_empty():
    with pytest.raises(ValueError):
        FakePerson(id=1, name="   ", age=20)


def test_person_invalid_name_type():
    with pytest.raises(TypeError):
        FakePerson(id=1, name=123, age=20)


def test_person_valid_name_setter(person):
    person.name = "Bob"
    assert person.name == "Bob"


# ---------------------------------------------------------
# TESTES DE AGE
# ---------------------------------------------------------
def test_person_invalid_age_type(person):
    with pytest.raises(TypeError):
        person.age = "30"


def test_person_invalid_age_negative(person):
    with pytest.raises(ValueError):
        person.age = -1


def test_person_invalid_age_over_limit(person):
    with pytest.raises(ValueError):
        person.age = 200


def test_person_valid_age(person):
    person.age = 45
    assert person.age == 45


# ---------------------------------------------------------
# TESTES DE MÉTODOS AUXILIARES
# ---------------------------------------------------------
def test_person_str():
    p = FakePerson(name="Ana", age=25)
    assert str(p) == "Ana, 25 anos"


def test_person_timestamp():
    p = FakePerson(name="Ana", age=25)
    assert isinstance(p.timestamp, datetime)
