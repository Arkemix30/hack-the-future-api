from typing import Any

from pydantic import SecretStr

from app.core.settings.base_settings import BaseConfig


class AppConfig(BaseConfig):
    debug: bool = False
    SECRET_KEY: SecretStr
    PROJECT_NAME: str = "hacker-the-future-api"
    API_V1_STR: str = "/api"

    class Config:
        validate_assignment = True

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return {"debug": self.debug}
