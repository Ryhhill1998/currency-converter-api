import httpx

from src.clients.ecb.ecb_client import EcbClient
from src.clients.ecb.http_ecb_client import HttpEcbClient
from src.clients.ecb.local_ecb_client import LocalEcbClient
from src.models.settings import Settings
from src.services.ingestion_service import IngestionService
from src.stores.archive.archive_store import ArchiveStore
from src.stores.rates.rates_store import RatesStore


class IngestionServiceContainer:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def _select_ecb_client(self, is_local: bool) -> EcbClient:
        if is_local:
            return LocalEcbClient(self.settings.ecb_local_file_path)

        return HttpEcbClient(
            client=httpx.Client(),
            url=self.settings.ecb_http_url.unicode_string(),
            data_format=self.settings.ecb_http_format,
            observations=self.settings.ecb_http_observations,
        )

    def _select_archive_store(self, is_local: bool) -> ArchiveStore:
        if is_local:
            from src.stores.archive.local_archive_store import LocalArchiveStore
            return LocalArchiveStore(base_path=self.settings.local_archive_base_path)

        from src.stores.archive.s3_archive_store import S3ArchiveStore
        return S3ArchiveStore(bucket=self.settings.s3_bucket_name)

    def _select_rates_store(self, is_local: bool) -> RatesStore:
        pass

    def get_ingestion_service(self) -> IngestionService:
        return IngestionService(
            ecb_client=self._select_ecb_client(self.settings.is_local_ecb_client),
            archive_store=self._select_archive_store(self.settings.is_local_archive_store),
            rates_store=self._select_rates_store(self.settings.is_local_rates_store),
        )
