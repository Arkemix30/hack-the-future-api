import random
from datetime import datetime as dt

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.definitions import EmissionType, EnergyCategory, EnergyLocation
from app.models import Energy
from app.repositories import EnergyRepository


def test_get_consumo_promedio_mensual(
    client: TestClient, test_db_session: Session
):
    energy_repository = EnergyRepository(test_db_session)

    energy_list = []
    for i in range(12):
        energy = Energy(
            quantity=random.randint(30, 500),
            datetime=dt.now(),
            location=EnergyLocation.PLANTA_DE_ENVASADO,
            energy_category=random.choice(list(EnergyCategory)),
            emission_type=random.choice(list(EmissionType)),
        )

        energy_list.append(energy)

    try:
        test_db_session.add_all(energy_list)
        test_db_session.commit()
        [test_db_session.refresh(energy) for energy in energy_list]
    except Exception as e:
        test_db_session.rollback()
        raise e

    response = client.get("/api/energy/consumo_promedio_mensual?year=2023")
    body = response.json()

    assert response.status_code == 200
    assert isinstance(body["data"], float)
