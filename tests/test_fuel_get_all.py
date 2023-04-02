import random
from datetime import datetime as dt

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.definitions import EmissionType, FuelType
from app.models import Fuel
from app.repositories import FuelRepository


def test_route_empty_response(client: TestClient, test_db_session: Session):
    """
    Test route to get empty list of Fuels.
    """
    response = client.get("/api/fuel")
    body = response.json()

    assert response.status_code == 200
    assert len(body) == 0


def test_route_response(client: TestClient, test_db_session: Session):
    fuel_repository = FuelRepository(test_db_session)
    fuel = Fuel(
        quantity=random.randint(30, 500),
        datetime=dt.now(),
        fuel_type=random.choice(list(FuelType)),
        emission_type=random.choice(list(EmissionType)),
    )
    fuel_repository.create(fuel)

    response = client.get("/api/fuel")
    body = response.json()

    assert response.status_code == 200
    assert len(body) == 1
