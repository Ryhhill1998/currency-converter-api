from typing import Generator

import pytest
import httpx
from freezegun import freeze_time
from mypy_boto3_s3.client import S3Client
from pydantic import HttpUrl
import polars as pl

from src.index import handler
from src.models.settings import Settings
from tests.e2e.constants import ARCHIVE_BUCKET_NAME


@pytest.fixture
def mock_ecb_data_df() -> pl.DataFrame:
    return pl.DataFrame(
        [
            {
                "CURRENCY": "B",
                "CURRENCY_DENOM": "A",
                "TIME_PERIOD": "2020-10-30",
                "OBS_VALUE": 91.5953
            },
            {
                "CURRENCY": "C",
                "CURRENCY_DENOM": "A",
                "TIME_PERIOD": "2026-03-27",
                "OBS_VALUE": 1.6731
            },
            {
                "CURRENCY": "D",
                "CURRENCY_DENOM": "A",
                "TIME_PERIOD": "2025-12-31",
                "OBS_VALUE": 1.9558
            },
            {
                "CURRENCY": "E",
                "CURRENCY_DENOM": "A",
                "TIME_PERIOD": "2026-03-27",
                "OBS_VALUE": 19.2158
            },
        ]
    )


@pytest.fixture
def mock_ecb_data_bytes(mock_ecb_data_df: pl.DataFrame) -> bytes:
    return mock_ecb_data_df.write_csv().encode(encoding="utf-8")


@pytest.fixture
def mock_ecb_data_dicts(mock_ecb_data_df: pl.DataFrame) -> list[dict]:
    return mock_ecb_data_df.to_dicts()


@pytest.fixture
def mock_ecb_url() -> str:
    return "https://test.com"


@pytest.fixture
def mock_settings(mock_ecb_url: str) -> Settings:
    return Settings(
        is_local_ecb_client=False,  # make sure to not hit actual API (mock client)
        is_local_vault_store=False,  # store in mocked AWS resources
        is_local_live_store=False,  # store in mocked AWS resources
        http_ecb_url=HttpUrl(mock_ecb_url),
        s3_archive_bucket_name=ARCHIVE_BUCKET_NAME,
    )


@pytest.fixture
def mock_ecb_endpoint_response(
    respx_mock, mock_ecb_url: str, mock_ecb_data_bytes: bytes
) -> Generator[None]:
    mock_response = httpx.Response(status_code=201, content=mock_ecb_data_bytes)
    respx_mock.get(mock_ecb_url).mock(return_value=mock_response)
    yield


@freeze_time("2026-01-01")
def test_handler_stores_expected_raw_data(
    mock_settings: Settings,
    mock_ecb_endpoint_response: None,
    mock_ecb_data_dicts: list[dict],
    create_archive_bucket: None,
    s3_client: S3Client,
) -> None:
    # ACT
    handler("", "", settings=mock_settings)

    # ASSERT
    archive_file_path = "rates/type=raw/year=2026/month=01/day=01/raw_rates.csv"
    actual_data = pl.read_csv(
        s3_client.get_object(Bucket=ARCHIVE_BUCKET_NAME, Key=archive_file_path)["Body"]
        .read()
    ).to_dicts()

    assert actual_data == mock_ecb_data_dicts


@freeze_time("2026-01-01")
def test_handler_stores_expected_parsed_data(
    mock_settings: Settings,
    mock_ecb_endpoint_response: None,
    mock_ecb_data_dicts: list[dict],
    create_archive_bucket: None,
    s3_client: S3Client,
) -> None:
    # ACT
    handler("", "", settings=mock_settings)

    # ASSERT
    archive_file_path = "rates/type=parsed/year=2026/month=01/day=01/parsed_rates.json"
    actual_data = pl.read_json(
        s3_client.get_object(Bucket=ARCHIVE_BUCKET_NAME, Key=archive_file_path)["Body"]
        .read()
    ).to_dicts()

    assert actual_data == mock_ecb_data_dicts


@pytest.mark.skip
def test_handler_stores_expected_live_data(
    mock_settings: Settings, create_archive_bucket: None
) -> None:
    handler("", "", settings=mock_settings)
