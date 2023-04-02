import os
import sys

import pytest
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.create_app import create_app
from app.infrastructure import get_db_session

load_dotenv()


@pytest.fixture
def test_db_session():
    engine = create_engine(
        os.environ.get(
            "TEST_DATABASE_URL",
            "postgresql://postgres:postgres@localhost:5432/postgres",
        )
    )
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as err:
        print(err)

    connection = engine.connect()
    transaction = connection.begin()
    session = Session(connection)
    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def app():
    app = create_app(test=True)
    return app


@pytest.fixture
def client(app: FastAPI, test_db_session):
    def _get_test_db():
        try:
            yield test_db_session
        finally:
            pass

    app.dependency_overrides[get_db_session] = _get_test_db
    with TestClient(app) as client:
        yield client
