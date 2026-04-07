from functools import lru_cache

from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # --- Mode Toggles ---
    is_local_ecb_client: bool = False
    is_local_archive_store: bool = False
    is_local_rates_store: bool = False

    # --- General ---
    http_timeout: float = 10.0

    # --- Local ECB Settings ---
    ecb_local_file_path: str = "data/ecb_sample.csv"

    # --- HTTP ECB Settings ---
    ecb_http_url: HttpUrl = HttpUrl("https://data-api.ecb.europa.eu/service/data/EXR/D..EUR.SP00.A")
    ecb_http_format: str = "csvdata"
    ecb_http_observations: int = 1


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore
