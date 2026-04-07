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
    http_ecb_url: HttpUrl = HttpUrl("https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml")
    http_ecb_format: str = "csvdata"
    http_ecb_observations: int = 1
    local_ecb_file_path: str = "./data/ecb_mock.csv"

    # --- Archive Store (S3) Settings ---
    s3_archive_bucket_name: str = "currency-ingestion-archive"
    local_archive_dir_path: str = "data/archive"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore
