# pylint: disable=missing-module-docstring
# pylint: disable=too-few-public-methods
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """ Settings class """
    logger: str = "logging"
    log_level: str = "DEBUG"
    debug_timing: bool = False

    fastapi_app: str = "app.main.app"
    app_env: str = Field(..., env="APP_ENV")
    api_prefix: str = Field(..., env="API_PREFIX")
    allowed_hosts: str = Field(..., env="ALLOWED_HOSTS")
    time_zone: str = "UTC"

    class Config:
        """ Config class"""
        env_file = ".env"


settings = Settings()

