import random
from datetime import datetime as dt

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.definitions import EmissionType, EnergyCategory, EnergyLocation


def test_create_record(client: TestClient, test_db_session: Session):
    """
    Test route to create a new Energy record.
    """

    response = client.post(
        "/api/energy",
        json={
            "quantity": random.randint(30, 500),
            "datetime": dt.now().isoformat(),
            "location": EnergyLocation.PLANTA_DE_ENVASADO,
            "energy_category": random.choice(list(EnergyCategory)),
            "emission_type": random.choice(list(EmissionType)),
        },
    )
    body = response.json()

    assert response.status_code == 200
