import random
from datetime import datetime as dt

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.definitions import EmissionType, FuelType, EnergyCategory, EnergyLocation, OilCategory, OilType
from app.models import Energy, Fuel, Oil


def test_comparativa_energia_combustible(client: TestClient, test_db_session: Session):

    energy = Energy(
        quantity=random.randint(1, 300),
        datetime=dt.now(),
        energy_category=random.choice(list(EnergyCategory)),
        energy_location=random.choice(list(EnergyLocation)),
        emission_type=random.choice(list(EmissionType))
    )

    fuel = Fuel(
        quantity=random.randint(1, 300),
        datetime=dt.now(),
        fuel_type=random.choice(list(FuelType)),
        emission_type=random.choice(list(EmissionType))
    )

    try:
        test_db_session.add(energy)
        test_db_session.add(fuel)
        test_db_session.commit()
    except Exception as e:
        test_db_session.rollback()
        raise e

    response = client.get("/api/comparativa_energia_combustible?year=2023")
    body = response.json()

    assert response.status_code == 200


def test_comparativa_energia_combustible_not_found(client: TestClient, test_db_session: Session):
    response = client.get("/api/comparativa_energia_combustible?year=2000")
    body = response.json()

    assert response.status_code == 404
    assert body["detail"] == "No data found for requested year"


def test_promedio_mensual_petroleo(client: TestClient, test_db_session: Session):

    fuel = Fuel(
        quantity=random.randint(1, 300),
        datetime=dt.now(),
        fuel_type=random.choice(list(FuelType)),
        emission_type=random.choice(list(EmissionType))
    )

    oil_list = []
    for i in range(24):
        oil = Oil(
            quantity=random.randint(1, 300),
            datetime=dt.now(),
            oil_type=random.choice(list(OilType)),
            oil_category=random.choice(list(OilCategory)),
            emission_type=random.choice(list(EmissionType))
        )
        oil_list.append(oil)


    try:
        test_db_session.add(fuel)
        test_db_session.add_all(oil_list)
        test_db_session.commit()
        test_db_session.refresh(fuel)
        [test_db_session.refresh(oil) for oil in oil_list]    
    except Exception as e:
        test_db_session.rollback()
        raise e

    response = client.get("/api/promedio_mensual_petroleo?year=2023")
    body = response.json()

    assert response.status_code == 200
    assert body["data"][OilType.ACEITE.value] > 0
    assert body["data"][OilType.REFRIGERANTE.value] > 0
    assert body["data"]["COMBUSTIBLE"] > 0

def test_promedio_mensual_petroleo_vacio(client: TestClient, test_db_session: Session):
    response = client.get("/api/promedio_mensual_petroleo?year=2000")
    body = response.json()

    assert response.status_code == 200
    assert body["data"][OilType.ACEITE.value] == 0
    assert body["data"][OilType.REFRIGERANTE.value] == 0
    assert body["data"]["COMBUSTIBLE"] == 0