import random
from datetime import datetime as dt

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.definitions import EmissionType, FuelType
from app.models import Fuel
from app.repositories import FuelRepository


def test_consumo_anual_por_categoria(
    client: TestClient, test_db_session: Session
):
    fuel_repository = FuelRepository(test_db_session)
    fuel = Fuel(
        quantity=random.randint(30, 500),
        datetime=dt.now(),
        fuel_type=random.choice(list(FuelType)),
        emission_type=random.choice(list(EmissionType)),
    )
    fuel_repository.create(fuel)

    response = client.get("/api/fuel/consumo_anual_por_categoria/?year=2023")

    assert response.status_code == 200


def test_consumo_mensual_por_categoria_vacio(
    client: TestClient, test_db_session: Session
):
    fuel_repository = FuelRepository(test_db_session)
    fuel = Fuel(
        quantity=random.randint(30, 500),
        datetime=dt.now(),
        fuel_type=random.choice(list(FuelType)),
        emission_type=random.choice(list(EmissionType)),
    )
    fuel_repository.create(fuel)

    response = client.get("/api/fuel/consumo_anual_por_categoria/?year=2000")

    assert response.status_code == 200
    assert (
        response.json()["data"][FuelType.COMBUSTIBLE_ADMINISTRATIVO.value] == 0
    )
    assert (
        response.json()["data"][FuelType.COMBUSTIBLE_DE_LOGISTICA.value] == 0
    )
    assert (
        response.json()["data"][
            FuelType.COMBUSTIBLE_INDIRECTO_DE_PROVEEDOR.value
        ]
        == 0
    )

    assert response.status_code == 200


def test_consumo_promedio_mensual(
    client: TestClient, test_db_session: Session
):
    fuel_list = []
    for i in range(12):
        fuel = Fuel(
            quantity=random.randint(30, 500),
            datetime=dt.now(),
            fuel_type=random.choice(list(FuelType)),
            emission_type=random.choice(list(EmissionType)),
        )
        fuel_list.append(fuel)

    try:
        test_db_session.add_all(fuel_list)
        test_db_session.commit()
        [test_db_session.refresh(fuel) for fuel in fuel_list]
    except Exception as e:
        test_db_session.rollback()
        raise e

    response = client.get("/api/fuel/consumo_promedio_mensual/?year=2023")

    assert response.status_code == 200
    assert isinstance(response.json()["data"], float)


def test_consumo_promedio_mensual_vacio(
    client: TestClient, test_db_session: Session
):
    fuel_list = []
    for i in range(12):
        fuel = Fuel(
            quantity=random.randint(30, 500),
            datetime=dt.now(),
            fuel_type=random.choice(list(FuelType)),
            emission_type=random.choice(list(EmissionType)),
        )
        fuel_list.append(fuel)

    try:
        test_db_session.add_all(fuel_list)
        test_db_session.commit()
        [test_db_session.refresh(fuel) for fuel in fuel_list]
    except Exception as e:
        test_db_session.rollback()
        raise e

    response = client.get("/api/fuel/consumo_promedio_mensual/?year=2000")

    assert response.status_code == 200
    assert response.json()["data"] == 0


def test_porcentaje_por_segmento_anual(
    client: TestClient, test_db_session: Session
):
    fuel_list = []
    for i in range(12):
        fuel = Fuel(
            quantity=random.randint(30, 500),
            datetime=dt.now(),
            fuel_type=random.choice(list(FuelType)),
            emission_type=random.choice(list(EmissionType)),
        )
        fuel_list.append(fuel)

    try:
        test_db_session.add_all(fuel_list)
        test_db_session.commit()
        [test_db_session.refresh(fuel) for fuel in fuel_list]
    except Exception as e:
        test_db_session.rollback()
        raise e

    response = client.get("/api/fuel/porcentaje_por_segmento_anual/?year=2023")

    assert response.status_code == 200


def test_porcentaje_por_segmento_anual_vacio(
    client: TestClient, test_db_session: Session
):
    fuel_list = []
    for i in range(12):
        fuel = Fuel(
            quantity=random.randint(30, 500),
            datetime=dt.now(),
            fuel_type=random.choice(list(FuelType)),
            emission_type=random.choice(list(EmissionType)),
        )
        fuel_list.append(fuel)

    try:
        test_db_session.add_all(fuel_list)
        test_db_session.commit()
        [test_db_session.refresh(fuel) for fuel in fuel_list]
    except Exception as e:
        test_db_session.rollback()
        raise e

    response = client.get("/api/fuel/porcentaje_por_segmento_anual/?year=2000")

    assert response.status_code == 200
    assert response.json()["data"][EmissionType.EMISIONES_DIRECTAS.value] == 0
    assert (
        response.json()["data"][EmissionType.EMISIONES_INDIRECTAS.value] == 0
    )
    assert (
        response.json()["data"][EmissionType.OTRAS_EMISIONES_INDIRECTAS.value]
        == 0
    )
