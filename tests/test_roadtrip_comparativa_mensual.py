import random
from datetime import datetime as dt

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.definitions import EmissionType, RoadtripGroupType
from app.models import Roadtrip
from app.repositories import RoadtripRepository


def test_comparativa_mensual(client: TestClient, test_db_session: Session):
    roadtrips_list = []
    for i in range(0, 36):
        road = Roadtrip(
            quantity=random.randint(1, 30),
            datetime=dt.now(),
            group=random.choice(list(RoadtripGroupType)),
            emission_type=random.choice(list(EmissionType))
        )
        roadtrips_list.append(road)

    try:
        test_db_session.add_all(roadtrips_list)
        test_db_session.commit()
        [test_db_session.refresh(roadtrip) for roadtrip in roadtrips_list]
    except Exception as e:
        test_db_session.rollback()
        raise e
    
    response = client.get("/api/roadtrip/comparativa_promedio_mensual?year=2023")
    body = response.json()

    assert response.status_code == 200
    assert isinstance(body["data"][RoadtripGroupType.EQUIPO_ADMINISTRATIVO.value], int)

def test_comparativa_mensual_vacio(client: TestClient, test_db_session: Session):
    response = client.get("/api/roadtrip/comparativa_promedio_mensual?year=2000")
    body = response.json()

    assert response.status_code == 200
    assert body["data"][RoadtripGroupType.EQUIPO_ADMINISTRATIVO.value] == 0
    assert body["data"][RoadtripGroupType.EQUIPO_DE_VENTAS.value] == 0
