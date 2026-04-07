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

    # --- ECB Client Settings ---
    ecb_http_url: HttpUrl = HttpUrl("https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml")
    ecb_http_format: str = "csvdata"
    ecb_http_observations: int = 1
    ecb_local_file_path: str = "./data/ecb_mock.csv"

    # --- Archive Store (S3) Settings ---
    s3_bucket_name: str = "currency-ingestion-archive"
    local_archive_base_path: str = "./tmp/archive"

    # --- Rates Store (Redis) Settings ---
    redis_url: str = "redis://localhost:6379/0"
    redis_key_prefix: str = "rates"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore
