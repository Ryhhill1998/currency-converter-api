from src.clients.ecb.ecb_client import EcbClient
from src.stores.archive.archive_store import ArchiveStore
from src.stores.rates.rates_store import RatesStore
from src.utils.parsers import parse_ecb_rates


class IngestionService:
    def __init__(self, ecb_client: EcbClient, archive_store: ArchiveStore, rates_store: RatesStore) -> None:
        self.ecb_client = ecb_client
        self.archive_store = archive_store
        self.rates_store = rates_store

    async def run(self) -> None:
        # Retrieve latest raw data from ECB
        latest_rates_data: bytes = await self.ecb_client.fetch_latest_rates()

        # Store raw data in archive
        self.archive_store.write(latest_rates_data)

        # Parse raw data into df
        parsed_rates: list[dict] = parse_ecb_rates(latest_rates_data)

        # Store parsed data
        self.rates_store.write(parsed_rates)
