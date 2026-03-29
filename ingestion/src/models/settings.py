from functools import lru_cache

from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class EcbDataSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ECB_DATA_")

    url: HttpUrl
    format: str = "csvdata"
    observations: int = 1


@lru_cache(maxsize=1)
def get_ecb_data_settings() -> EcbDataSettings:
    return EcbDataSettings()  # type: ignore
