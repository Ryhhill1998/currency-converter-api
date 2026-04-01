from functools import lru_cache

from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class GeneralSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GENERAL_")

    is_local_ecb_client: bool = False
    is_local_archive_store: bool = False
    is_local_rates_store: bool = False

    http_timeout: float = 10.0


class LocalEcbSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="LOCAL_ECB_")


class HttpEcbSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="HTTP_ECB_")

    url: HttpUrl
    format: str = "csvdata"
    observations: int = 1


@lru_cache(maxsize=1)
def get_general_settings() -> GeneralSettings:
    return GeneralSettings()  # type: ignore


@lru_cache(maxsize=1)
def get_local_ecb_settings() -> LocalEcbSettings:
    return LocalEcbSettings()  # type: ignore


@lru_cache(maxsize=1)
def get_http_ecb_settings() -> HttpEcbSettings:
    return HttpEcbSettings()  # type: ignore
