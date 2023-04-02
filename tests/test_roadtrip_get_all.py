import random
from datetime import datetime as dt

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.definitions import EmissionType, RoadtripGroupType
from app.models import Roadtrip
from app.repositories import RoadtripRepository


def test_route_empty_response(client: TestClient, test_db_session: Session):
    """
    Test route to get empty list of roadtrips.s
    """
    response = client.get("/api/roadtrip")
    body = response.json()

    assert response.status_code == 200
    assert len(body) == 0


def test_route_response(client: TestClient, test_db_session: Session):
    roadtrip_repo = RoadtripRepository(test_db_session)
    road = Roadtrip(
        quantity=random.randint(1, 300),
        datetime=dt.now(),
        group=random.choice(list(RoadtripGroupType)),
        emission_type=random.choice(list(EmissionType))
    )
    roadtrip_repo.create(road)

    response = client.get("/api/roadtrip")
    body = response.json()

    assert response.status_code == 200
    assert len(body) == 1
