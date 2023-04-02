import random
from datetime import datetime as dt

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.definitions import EmissionType, OilType, OilCategory
from app.models import Oil
from app.repositories import OilRepository


def test_consumo_mensual_aceite(client: TestClient, test_db_session: Session):

    oil_repository = OilRepository(test_db_session)
    oil = Oil(
        quantity=random.randint(1, 300),
        datetime=dt.now(),
        oil_type=random.choice(list(OilType)),
        oil_category=random.choice(list(OilCategory)),
        emission_type=random.choice(list(EmissionType))
    )
    oil_repository.create(oil)

    response = client.get("/api/oil/consumo_mensual_aceite?year=2023")
    body = response.json()

    assert response.status_code == 200
    assert len(body["data"]) > 0


def test_consumo_mensual_aceite_vacio(client: TestClient, test_db_session: Session):

    response = client.get("/api/oil/consumo_mensual_aceite?year=2000")
    body = response.json()

    assert response.status_code == 200
