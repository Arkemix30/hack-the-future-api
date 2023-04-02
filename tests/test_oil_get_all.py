import random
from datetime import datetime as dt

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.definitions import EmissionType, OilType, OilCategory
from app.models import Oil
from app.repositories import OilRepository


def test_route_empty_response(client: TestClient, test_db_session: Session):
    """
    Test route to get empty list of Oils.
    """
    response = client.get("/api/oil")
    body = response.json()

    assert response.status_code == 200
    assert len(body) == 0


def test_route_response(client: TestClient, test_db_session: Session):
    oil_repository = OilRepository(test_db_session)
    oil = Oil(
        quantity=random.randint(1, 300),
        datetime=dt.now(),
        oil_type=random.choice(list(OilType)),
        oil_category=random.choice(list(OilCategory)),
        emission_type=random.choice(list(EmissionType))
    )
    oil_repository.create(oil)

    response = client.get("/api/oil")
    body = response.json()

    assert response.status_code == 200
    assert len(body) == 1
