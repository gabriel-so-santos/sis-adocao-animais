import pytest
from datetime import datetime, timedelta, timezone

from domain.adoptions.reservation_queue import ReservationQueue

# ---------------------------------------------------------
# FIXTURE: RESERVA VÁLIDA
# ---------------------------------------------------------
@pytest.fixture
def reservation():
    return ReservationQueue(
        animal_id=1,
        adopter_id=2,
        compatibility_rate=85.5,
        is_canceled=False,
        id=10,
        timestamp=datetime.now(timezone.utc)
    )

# ---------------------------------------------------------
# TESTES DE INICIALIZAÇÃO
# ---------------------------------------------------------
def test_reservation_initialization(reservation):
    assert reservation.animal_id == 1
    assert reservation.adopter_id == 2
    assert reservation.compatibility_rate == 85.5
    assert reservation.is_canceled is False
    assert reservation.id == 10
    assert isinstance(reservation.timestamp, datetime)


# ---------------------------------------------------------
# TESTES DE VALIDAÇÃO
# ---------------------------------------------------------

def test_invalid_animal_id_type():
    with pytest.raises(TypeError):
        ReservationQueue(
            animal_id="1",
            adopter_id=1,
            compatibility_rate=50
        )


def test_invalid_animal_id_value():
    with pytest.raises(ValueError):
        ReservationQueue(
            animal_id=0,
            adopter_id=1,
            compatibility_rate=50
        )


def test_invalid_adopter_id_type():
    with pytest.raises(TypeError):
        ReservationQueue(
            animal_id=1,
            adopter_id="2",
            compatibility_rate=50
        )


def test_invalid_adopter_id_value():
    with pytest.raises(ValueError):
        ReservationQueue(
            animal_id=1,
            adopter_id=0,
            compatibility_rate=50
        )


def test_invalid_compatibility_rate_type():
    with pytest.raises(TypeError):
        ReservationQueue(
            animal_id=1,
            adopter_id=2,
            compatibility_rate="alta"
        )


def test_invalid_compatibility_rate_below_zero():
    with pytest.raises(ValueError):
        ReservationQueue(
            animal_id=1,
            adopter_id=2,
            compatibility_rate=-1
        )


def test_invalid_compatibility_rate_above_limit():
    with pytest.raises(ValueError):
        ReservationQueue(
            animal_id=1,
            adopter_id=2,
            compatibility_rate=120
        )


def test_valid_compatibility_rate_int():
    rq = ReservationQueue(
        animal_id=1,
        adopter_id=2,
        compatibility_rate=80
    )
    assert rq.compatibility_rate == 80.0

def test_invalid_is_canceled_type(reservation):
    with pytest.raises(TypeError):
        reservation.is_canceled = "false"


def test_valid_is_canceled_change(reservation):
    reservation.is_canceled = True
    assert reservation.is_canceled is True

# ---------------------------------------------------------
# TESTES DE ORDENAÇÃO (__lt__)
# ---------------------------------------------------------
def test_reservation_higher_compatibility_has_priority():
    r1 = ReservationQueue(
        animal_id=1,
        adopter_id=1,
        compatibility_rate=90,
        timestamp=datetime.now(timezone.utc)
    )
    r2 = ReservationQueue(
        animal_id=1,
        adopter_id=2,
        compatibility_rate=70,
        timestamp=datetime.now(timezone.utc)
    )

    assert r1 < r2


def test_reservation_same_compatibility_older_first():
    now = datetime.now(timezone.utc)

    r1 = ReservationQueue(
        animal_id=1,
        adopter_id=1,
        compatibility_rate=80,
        timestamp=now
    )
    r2 = ReservationQueue(
        animal_id=1,
        adopter_id=2,
        compatibility_rate=80,
        timestamp=now + timedelta(minutes=5)
    )

    assert r1 < r2


# ---------------------------------------------------------
# TESTES DE EXPIRAÇÃO
# ---------------------------------------------------------
def test_reservation_not_expired(monkeypatch):
    monkeypatch.setattr(
        "domain.adoptions.reservation_queue.duration_hours",
        2
    )

    rq = ReservationQueue(
        animal_id=1,
        adopter_id=1,
        compatibility_rate=60,
        timestamp=datetime.now(timezone.utc)
    )

    assert rq.check_expiration() is False


def test_reservation_expired(monkeypatch):
    monkeypatch.setattr(
        "domain.adoptions.reservation_queue.duration_hours",
        1
    )

    past_time = datetime.now(timezone.utc) - timedelta(hours=2)

    rq = ReservationQueue(
        animal_id=1,
        adopter_id=1,
        compatibility_rate=60,
        timestamp=past_time
    )

    assert rq.check_expiration() is True
    assert rq.has_ended is True

