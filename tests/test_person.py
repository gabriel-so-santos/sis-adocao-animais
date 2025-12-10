import pytest
from domain.people.person import Person


# ---------------------------------------------------------
# Classe concreta para testar Person (pois é abstrata)
# ---------------------------------------------------------
class FakePerson(Person):
    pass


# ---------------------------------------------------------
# FIXTURE: cria uma pessoa válida
# ---------------------------------------------------------
@pytest.fixture
def person():
    return FakePerson(
        id=1,
        name="Alice",
        age=30
    )


# ---------------------------------------------------------
# TESTES DE ATRIBUTOS BÁSICOS
# ---------------------------------------------------------

def test_person_initialization(person):
    assert person.id == 1
    assert person.name == "Alice"
    assert person.age == 30


# ---------------------------------------------------------
# TESTES DO SETTER name
# ---------------------------------------------------------

def test_person_invalid_name_empty():
    with pytest.raises(ValueError):
        FakePerson(id=1, name="   ", age=20)


def test_person_invalid_name_not_string():
    with pytest.raises(TypeError):
        FakePerson(id=1, name=123, age=20)


def test_person_valid_name_setter(person):
    person.name = "Bob"
    assert person.name == "Bob"


# ---------------------------------------------------------
# TESTES DO SETTER age
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