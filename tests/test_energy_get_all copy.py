import random
from datetime import datetime as dt

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.definitions import EmissionType, EnergyCategory, EnergyLocation
from app.models import Energy
from app.repositories import EnergyRepository


def test_route_empty_response(client: TestClient, test_db_session: Session):
    """
    Test route to get empty list of Events.
    """
    response = client.get("/api/energy")
    body = response.json()

    assert response.status_code == 200
    assert len(body) == 0


def test_route_response(client: TestClient, test_db_session: Session):
    energy_repository = EnergyRepository(test_db_session)
    energy = Energy(
        quantity=random.randint(30, 500),
        datetime=dt.now(),
        location=EnergyLocation.PLANTA_DE_ENVASADO,
        energy_category=random.choice(list(EnergyCategory)),
        emission_type=random.choice(list(EmissionType)),
    )
    energy_repository.create(energy)

    response = client.get("/api/energy")
    body = response.json()

    assert response.status_code == 200
    assert len(body) == 1
