from unittest.mock import patch

import pytest

from src.index import handler
from src.models.settings import GeneralSettings


@pytest.fixture
def mock_settings() -> GeneralSettings:
    return GeneralSettings(
        is_local_ecb_client=True,  # make sure to not hit actual API
        is_local_archive_store=False,  # store in mocked AWS resources
        is_local_rates_store=False,  # store in mocked AWS resources
    )


@pytest.mark.asyncio
async def test_handler_stores_expected_archive_data(mock_settings: GeneralSettings) -> None:
    with patch("src.index.get_general_settings", return_value=mock_settings):
        await handler("", "")


@pytest.mark.asyncio
async def test_handler_stores_expected_rates_data(mock_settings: GeneralSettings) -> None:
    with patch("src.index.get_general_settings", return_value=mock_settings):
        await handler("", "")
