import json
from datetime import datetime
from enum import StrEnum, auto

from src.clients.ecb.ecb_client import EcbClient
from src.stores.vault.vault_store import VaultStore
from src.stores.live.live_store import LiveStore
from src.utils.parsers import parse_raw_rates, serialise_rates


class VaultDataType(StrEnum):
    RAW = auto()
    PARSED = auto()


class VaultFileExtension(StrEnum):
    CSV = auto()
    JSON = auto()


class IngestionService:
    def __init__(self, ecb_client: EcbClient, vault_store: VaultStore, live_store: LiveStore) -> None:
        self.ecb_client = ecb_client
        self.vault_store = vault_store
        self.live_store = live_store

    @staticmethod
    def _generate_vault_path(timestamp: datetime, data_type: VaultDataType, file_extension: VaultFileExtension) -> str:
        date_path = timestamp.strftime("year=%Y/month=%m/day=%d")
        return f"ecb/type={data_type.value}/{date_path}/{data_type.value}_rates.{file_extension}"

    def run(self, run_timestamp: datetime) -> None:
        # Retrieve latest raw data from ECB
        raw_rates: bytes = self.ecb_client.fetch_latest_rates()

        # Store raw data in vault
        raw_file_path: str = self._generate_vault_path(
            timestamp=run_timestamp, data_type=VaultDataType.RAW, file_extension=VaultFileExtension.CSV
        )
        self.vault_store.store(data=raw_rates, file_path=raw_file_path)

        # Parse raw data
        parsed_rates: list[dict] = parse_raw_rates(raw_rates)

        # Store parsed data in vault
        parsed_file_path: str = self._generate_vault_path(
            timestamp=run_timestamp, data_type=VaultDataType.PARSED, file_extension=VaultFileExtension.JSON
        )
        serialised_rates: bytes = serialise_rates(parsed_rates)
        self.vault_store.store(data=serialised_rates, file_path=parsed_file_path)

        # Store parsed data in cache
        # self.live_store.write(parsed_rates)
