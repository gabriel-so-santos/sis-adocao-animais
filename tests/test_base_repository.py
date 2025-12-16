import pytest
from unittest.mock import MagicMock
from sqlalchemy.exc import IntegrityError

from infrastructure.repositories.base_repo import BaseRepository

# ---------------------------------------------------------
# MODELO SQLALCHEMY FAKE
# ---------------------------------------------------------
class FakeColumn:
    def __init__(self, name):
        self.name = name


class FakeTable:
    columns = [
        FakeColumn("id"),
        FakeColumn("name"),
        FakeColumn("age"),
    ]


class FakeModel:
    __table__ = FakeTable()

    def __init__(self, id=None, name=None, age=None):
        self.id = id
        self.name = name
        self.age = age

# ---------------------------------------------------------
# ENTIDADE DE DOMÍNIO FAKE
# ---------------------------------------------------------
class FakeDomain:
    def __init__(self, id=None, name=None, age=None):
        self.id = id
        self.name = name
        self.age = age

# ---------------------------------------------------------
# REPOSITÓRIO CONCRETO PARA TESTE
# ---------------------------------------------------------
class FakeRepository(BaseRepository):
    domain_class = FakeDomain

# ---------------------------------------------------------
# FIXTURES
# ---------------------------------------------------------
@pytest.fixture
def session():
    session = MagicMock()
    session.query.return_value.all.return_value = []
    return session


@pytest.fixture
def repository(session):
    return FakeRepository(session=session, model_class=FakeModel)


@pytest.fixture
def domain_obj():
    return FakeDomain(id=1, name="Alice", age=30)


@pytest.fixture
def model_obj():
    return FakeModel(id=1, name="Alice", age=30)

# ---------------------------------------------------------
# TESTES _to_domain
# ---------------------------------------------------------
def test_to_domain_with_none(repository):
    assert repository._to_domain(None) is None


def test_to_domain_success(repository, model_obj):
    domain = repository._to_domain(model_obj)

    assert isinstance(domain, FakeDomain)
    assert domain.id == 1
    assert domain.name == "Alice"
    assert domain.age == 30

# ---------------------------------------------------------
# TESTES _to_model
# ---------------------------------------------------------
def test_to_model_with_none(repository):
    assert repository._to_model(None) is None


def test_to_model_success(repository, domain_obj):
    model = repository._to_model(domain_obj)

    assert isinstance(model, FakeModel)
    assert model.id == 1
    assert model.name == "Alice"
    assert model.age == 30

# ---------------------------------------------------------
# TESTES SAVE
# ---------------------------------------------------------
def test_save_success(repository, domain_obj):
    repository.session.add.return_value = None

    result = repository.save(domain_obj)

    assert result is True
    repository.session.add.assert_called_once()
    repository.session.commit.assert_called_once()
    repository.session.refresh.assert_called_once()


def test_save_integrity_error(repository, domain_obj):
    repository.session.commit.side_effect = IntegrityError(None, None, None)

    result = repository.save(domain_obj)

    assert result is False
    repository.session.rollback.assert_called_once()

# ---------------------------------------------------------
# TESTES list_all
# ---------------------------------------------------------
def test_list_all(repository, model_obj):
    repository.session.query.return_value.all.return_value = [model_obj]

    result = repository.list_all()

    assert len(result) == 1
    assert isinstance(result[0], FakeDomain)

# ---------------------------------------------------------
# TESTES get_by_id
# ---------------------------------------------------------
def test_get_by_id_found(repository, model_obj):
    repository.session.get.return_value = model_obj

    result = repository.get_by_id(1)

    assert isinstance(result, FakeDomain)


def test_get_by_id_not_found(repository):
    repository.session.get.return_value = None

    result = repository.get_by_id(1)

    assert result is None

# ---------------------------------------------------------
# TESTES UPDATE
# ---------------------------------------------------------
def test_update_success(repository, domain_obj, model_obj):
    repository.session.merge.return_value = model_obj

    result = repository.update(domain_obj)

    assert result is True
    repository.session.merge.assert_called_once()
    repository.session.commit.assert_called_once()
    repository.session.refresh.assert_called_once()


def test_update_with_none_domain(repository):
    result = repository.update(None)
    assert result is False


# ---------------------------------------------------------
# TESTES DELETE
# ---------------------------------------------------------
def test_delete_by_success(repository, model_obj):
    repository.session.get.return_value = model_obj

    result = repository.delete_by(1)

    assert result is True
    repository.session.delete.assert_called_once()
    repository.session.commit.assert_called_once()


def test_delete_by_not_found(repository):
    repository.session.get.return_value = None

    result = repository.delete_by(1)

    assert result is False

