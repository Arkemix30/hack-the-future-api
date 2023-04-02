import random
from datetime import datetime as dt

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.definitions import EmissionType, FuelType


def test_create_record(client: TestClient, test_db_session: Session):
    """
    Test route to create a new Fuel record.
    """

    response = client.post(
        "/api/fuel",
        json={
            "quantity": random.randint(30, 500),
            "datetime": dt.now().isoformat(),
            "fuel_type": random.choice(list(FuelType)),
            "emission_type": random.choice(list(EmissionType)),
        },
    )
    body = response.json()

    assert response.status_code == 200


def test_create_invalid_emission_type(
    client: TestClient, test_db_session: Session
):
    """
    Test route to create a new Fuel record with invalid emission type.
    """

    response = client.post(
        "/api/fuel",
        json={
            "quantity": random.randint(30, 500),
            "datetime": dt.now().isoformat(),
            "fuel_type": random.choice(list(FuelType)),
            "emission_type": "invalid_emission_type",
        },
    )
    body = response.json()

    assert response.status_code == 422
    assert "value is not a valid" in body["detail"][0]["msg"]
