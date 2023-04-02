import random
from datetime import datetime as dt

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.definitions import EmissionType, RoadtripGroupType


def test_create_record(client: TestClient, test_db_session: Session):
    """
    Test route to create a new Oil record.
    """

    response = client.post(
        "/api/roadtrip",
        json={
            "quantity": random.randint(1, 30),
            "datetime": dt.now().isoformat(),
            "group": random.choice(list(RoadtripGroupType)),
            "emission_type": random.choice(list(EmissionType)),
        },
    )
    body = response.json()

    assert response.status_code == 200


def test_create_invalid_emission_type(
    client: TestClient, test_db_session: Session
):
    """
    Test route to create a new roadtrip record with invalid emission type.
    """

    response = client.post(
        "/api/roadtrip",
        json={
            "quantity": random.randint(1, 30),
            "datetime": dt.now().isoformat(),
            "group": random.choice(list(RoadtripGroupType)),
            "emission_type": "invalid_emission_type",
        },
    )
    body = response.json()

    assert response.status_code == 422
    assert "value is not a valid" in body["detail"][0]["msg"]
