from sqlmodel import Session, create_engine

from app.core.config import get_app_settings

app_settings = get_app_settings()

engine = create_engine(
    app_settings.DATABASE_URI, echo=app_settings.ENVIRONMENT == "dev"
)


def get_db_session() -> Session:
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
