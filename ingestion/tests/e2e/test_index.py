from typing import Generator

import pytest
import httpx
from freezegun import freeze_time
from mypy_boto3_s3.client import S3Client

from src.index import handler
from src.models.settings import Settings
from tests.e2e.constants import ARCHIVE_BUCKET_NAME


@pytest.fixture
def mock_ecb_url() -> str:
    return "https://test.com"


@pytest.fixture
def mock_settings(mock_ecb_url: str) -> Settings:
    return Settings(
        is_local_ecb_client=False,  # make sure to not hit actual API (mock client)
        is_local_vault_store=False,  # store in mocked AWS resources
        is_local_live_store=False,  # store in mocked AWS resources
        http_ecb_url=mock_ecb_url,
        s3_archive_bucket_name=ARCHIVE_BUCKET_NAME,
    )


@pytest.fixture
def mock_ecb_endpoint_response(respx_mock, mock_ecb_url: str) -> Generator[None]:
    with open("data/ecb/ecb_data.csv", "rb") as file:
        ecb_data: bytes = file.read()

    mock_response = httpx.Response(status_code=201, content=ecb_data)
    respx_mock.get(mock_ecb_url).mock(return_value=mock_response)
    yield


@freeze_time("2026-01-01")
def test_handler_stores_expected_archive_data(
    mock_settings: Settings, mock_ecb_endpoint_response: None, create_archive_bucket: None, s3_client: S3Client
) -> None:
    # ACT
    handler("", "", settings=mock_settings)

    # ASSERT
    archive_file_path = "rates/type=raw/year=2026/month=01/day=01/raw_rates.csv"
    data = s3_client.get_object(Bucket=ARCHIVE_BUCKET_NAME, Key=archive_file_path)["Body"].read().decode(encoding="utf-8")
    print(data)


@pytest.mark.skip
def test_handler_stores_expected_rates_data(
    mock_settings: Settings, create_archive_bucket: None
) -> None:
    handler("", "", settings=mock_settings)
