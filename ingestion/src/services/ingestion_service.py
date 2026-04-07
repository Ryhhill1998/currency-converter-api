from datetime import datetime

from src.clients.ecb.ecb_client import EcbClient
from src.stores.archive.archive_store import ArchiveStore
from src.stores.rates.rates_store import RatesStore
from src.utils.parsers import parse_ecb_rates


class IngestionService:
    def __init__(self, ecb_client: EcbClient, archive_store: ArchiveStore, rates_store: RatesStore) -> None:
        self.ecb_client = ecb_client
        self.archive_store = archive_store
        self.rates_store = rates_store

    @staticmethod
    def _generate_archive_path(timestamp: datetime) -> str:
        return timestamp.strftime("ecb/year=%Y/month=%m/day=%d/raw_rates.csv")

    def run(self, run_timestamp: datetime) -> None:
        # Retrieve latest raw data from ECB
        latest_rates_data: bytes = self.ecb_client.fetch_latest_rates()

        # Store raw data in archive
        archive_file_path: str = self._generate_archive_path(run_timestamp)
        self.archive_store.write(data=latest_rates_data, file_path=archive_file_path)

        # Parse raw data into df
        parsed_rates: list[dict] = parse_ecb_rates(latest_rates_data)

        # Store parsed data
        self.rates_store.write(parsed_rates)
