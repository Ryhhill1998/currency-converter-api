from src.clients.ecb.ecb_client import EcbClient
from src.stores.archive.archive_store import ArchiveStore
from src.stores.rates.rates_store import RatesStore


class IngestionService:
    def __init__(self, ecb_client: EcbClient, archive_store: ArchiveStore, rates_store: RatesStore) -> None:
        self.ecb_client = ecb_client
        self.archive_store = archive_store
        self.rates_store = rates_store

    def run(self) -> None:
        pass
