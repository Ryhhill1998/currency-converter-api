from typing import Generator
from unittest.mock import patch

import pytest
from freezegun import freeze_time
from mypy_boto3_s3.client import S3Client

from src.index import handler
from src.models.settings import Settings
from tests.e2e.constants import ARCHIVE_BUCKET_NAME


@pytest.fixture
def mock_settings() -> Settings:
    return Settings(
        is_local_ecb_client=False,  # make sure to not hit actual API (mock client)
        is_local_archive_store=False,  # store in mocked AWS resources
        is_local_rates_store=False,  # store in mocked AWS resources
        ecb_http_url="https://test.com",
    )


@freeze_time("2026-01-01")
@pytest.mark.asyncio
async def test_handler_stores_expected_archive_data(
    mock_settings: Settings, create_archive_bucket: None, s3_client: S3Client
) -> None:
    # ACT
    await handler("", "")

    # ASSERT
    archive_file_path = "ecb/year=2026/month=01/day=01/raw_rates.csv"
    data = s3_client.get_object(Bucket=ARCHIVE_BUCKET_NAME, Key=archive_file_path)["Body"].read().decode(encoding="utf-8")
    print(data)


@pytest.mark.asyncio
async def test_handler_stores_expected_rates_data(
    mock_settings: Settings, create_archive_bucket: None
) -> None:
    await handler("", "")
