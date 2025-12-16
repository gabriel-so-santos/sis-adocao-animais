import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta

from services.reservation_service import ReservationService
from domain.adoptions.reservation_queue import ReservationQueue
from domain.enums.animal_status import AnimalStatus
from domain.adoptions.adoption import Adoption

# ---------------------------------------------------------
# FIXTURES DE REPOSITÓRIOS MOCKADOS
# ---------------------------------------------------------
@pytest.fixture
def reservation_repo():
    return MagicMock()


@pytest.fixture
def animal_repo():
    return MagicMock()


@pytest.fixture
def adopter_repo():
    return MagicMock()


@pytest.fixture
def adoption_repo():
    return MagicMock()

# ---------------------------------------------------------
# FIXTURE DO SERVICE
# ---------------------------------------------------------
@pytest.fixture
def service(reservation_repo, animal_repo, adopter_repo, adoption_repo):
    return ReservationService(
        reservation_repo=reservation_repo,
        animal_repo=animal_repo,
        adopter_repo=adopter_repo,
        adoption_repo=adoption_repo
    )

# ---------------------------------------------------------
# TESTES list_reservations
# ---------------------------------------------------------
def test_list_reservations_groups_finished_and_ongoing(
    service, reservation_repo, animal_repo, adopter_repo
):
    now = datetime.now()

    r1 = ReservationQueue(
        animal_id=10,
        adopter_id=100,
        compatibility_rate=80,
        timestamp=now - timedelta(hours=5)
    )

    r2 = ReservationQueue(
        animal_id=10,
        adopter_id=101,
        compatibility_rate=70,
        timestamp=now - timedelta(hours=4)
    )

    reservation_repo.list_all.return_value = [r1, r2]
    animal_repo.get_by_id.return_value = MagicMock()
    adopter_repo.get_by_id.return_value = MagicMock()

    result = service.list_reservations()

    assert "finished" in result
    assert "ongoing" in result

# ---------------------------------------------------------
# TESTES prepare_reservation_form
# ---------------------------------------------------------
def test_prepare_form_with_no_selection(service, animal_repo, adopter_repo):
    animal_repo.list_reservable_animals.return_value = ["animal"]
    adopter_repo.list_all.return_value = ["adopter"]

    result = service.prepare_reservation_form()

    assert result["animals"] == ["animal"]
    assert result["adopters"] == ["adopter"]
    assert result["selected_animal"] is None
    assert result["selected_adopter"] is None

def test_prepare_form_with_selected_ids(service, animal_repo, adopter_repo):
    animal_repo.get_by_id.return_value = "animal"
    adopter_repo.get_by_id.return_value = "adopter"

    result = service.prepare_reservation_form(animal_id=1, adopter_id=2)

    assert result["selected_animal"] == "animal"
    assert result["selected_adopter"] == "adopter"

# ---------------------------------------------------------
# TESTES create_reservation
# ---------------------------------------------------------
def test_create_reservation_first_reservation_updates_status(
    service, reservation_repo, animal_repo, adopter_repo, monkeypatch
):
    reservation_repo.has_active_reservations.return_value = False
    reservation_repo.save.return_value = True

    animal_repo.get_by_id.return_value = MagicMock()
    adopter_repo.get_by_id.return_value = MagicMock()

    monkeypatch.setattr(
        "services.reservation_service.CompatibilityService.calculate_rate",
        lambda self, a, b: 85
    )

    service.create_reservation(animal_id=1, adopter_id=2)

    animal_repo.update_status.assert_called_once_with(
        id=1,
        new_status=AnimalStatus.RESERVED
    )

def test_create_reservation_duplicate_raises_error(
    service, reservation_repo, animal_repo, adopter_repo, monkeypatch
):
    reservation_repo.save.return_value = False
    reservation_repo.has_active_reservations.return_value = True

    animal_repo.get_by_id.return_value = MagicMock()
    adopter_repo.get_by_id.return_value = MagicMock()

    monkeypatch.setattr(
        "services.reservation_service.CompatibilityService.calculate_rate",
        lambda self, a, b: 50
    )

    with pytest.raises(ValueError):
        service.create_reservation(animal_id=1, adopter_id=2)

# ---------------------------------------------------------
# TESTES get_queue_ending_time
# ---------------------------------------------------------
def test_get_queue_ending_time(service, reservation_repo):
    first = MagicMock(timestamp=datetime(2024, 1, 1, 10, 0))
    reservation_repo.get_first_reservation.return_value = first

    ending = service.get_queue_ending_time(animal_id=1)

    assert isinstance(ending, datetime)

# ---------------------------------------------------------
# TESTES cancel_reservation
# ---------------------------------------------------------
def test_cancel_reservation_clears_queue_and_updates_status(
    service, reservation_repo, animal_repo
):
    reservation = MagicMock(animal_id=1)

    reservation_repo.get_by_id.return_value = reservation
    reservation_repo.all_canceled.return_value = True

    service.cancel_reservation(reservation_id=10)

    reservation_repo.clear_queue.assert_called_once_with(1)
    animal_repo.update_status.assert_called_once_with(
        id=1,
        new_status=AnimalStatus.AVAILABLE
    )

# ---------------------------------------------------------
# TESTES finalize_queue
# ---------------------------------------------------------
def test_finalize_queue_not_expired(service, reservation_repo):
    reservation_repo.is_queue_expired.return_value = False

    result = service.finalize_queue(animal_id=1)

    assert result is None

def test_finalize_queue_empty_queue(service, reservation_repo, animal_repo):
    reservation_repo.is_queue_expired.return_value = True
    reservation_repo.list_active_queue.return_value = []

    result = service.finalize_queue(animal_id=1)

    assert result is None
    animal_repo.update_status.assert_called_once_with(
        id=1,
        new_status=AnimalStatus.AVAILABLE
    )

def test_finalize_queue_returns_first(service, reservation_repo):
    reservation_repo.is_queue_expired.return_value = True
    reservation_repo.list_active_queue.return_value = ["reservation"]

    result = service.finalize_queue(animal_id=1)

    assert result == "reservation"


# ---------------------------------------------------------
# TESTES confirm_adoption
# ---------------------------------------------------------
def test_confirm_adoption_creates_adoption_and_updates_status(
    service, reservation_repo, animal_repo, adoption_repo, monkeypatch
):
    reservation = MagicMock(animal_id=1, adopter_id=2)
    reservation_repo.get_by_id.return_value = reservation

    animal_repo.get_by_id.return_value = MagicMock()

    monkeypatch.setattr(
        "services.reservation_service.AdoptionFeeService.calculate_fee",
        lambda self, animal: 120
    )

    service.confirm_adoption(reservation_id=10)

    animal_repo.update_status.assert_called_once_with(
        id=1,
        new_status=AnimalStatus.ADOPTED
    )

    adoption_repo.save.assert_called_once()
