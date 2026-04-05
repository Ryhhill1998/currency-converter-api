from typing import Generator
from unittest.mock import patch

import pytest
from mypy_boto3_s3.client import S3Client

from src.index import handler
from src.models.settings import GeneralSettings, HttpEcbSettings


@pytest.fixture
def mock_general_settings() -> GeneralSettings:
    return GeneralSettings(
        is_local_ecb_client=False,  # make sure to not hit actual API (mock client)
        is_local_archive_store=False,  # store in mocked AWS resources
        is_local_rates_store=False,  # store in mocked AWS resources
    )


@pytest.fixture
def mock_http_ecb_settings() -> HttpEcbSettings:
    return HttpEcbSettings(url="https://test.com")


@pytest.fixture
def mock_settings(mock_general_settings: GeneralSettings, mock_http_ecb_settings: HttpEcbSettings) -> Generator[None]:
    with (
        patch(target="src.index.get_general_settings", return_value=mock_general_settings),
        patch(
            target="src.containers.ingestion_service_container.get_http_ecb_settings",
            return_value=mock_http_ecb_settings,
        ),
    ):
        yield


@pytest.mark.asyncio
async def test_handler_stores_expected_archive_data(
    mock_settings: GeneralSettings, create_archive_bucket: None, s3_client: S3Client
) -> None:
    await handler("", "")


@pytest.mark.asyncio
async def test_handler_stores_expected_rates_data(
    mock_settings: GeneralSettings, create_archive_bucket: None
) -> None:
    with patch("src.index.get_general_settings", return_value=mock_settings):
        await handler("", "")
