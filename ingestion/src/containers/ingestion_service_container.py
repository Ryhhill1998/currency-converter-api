import httpx

from src.clients.ecb.ecb_client import EcbClient
from src.clients.ecb.http_ecb_client import HttpEcbClient
from src.models.settings import GeneralSettings, HttpEcbSettings, get_http_ecb_settings, get_local_ecb_settings, \
    LocalEcbSettings
from src.services.ingestion_service import IngestionService
from src.stores.archive.archive_store import ArchiveStore
from src.stores.rates.rates_store import RatesStore


class IngestionServiceContainer:
    def __init__(self, settings: GeneralSettings) -> None:
        self.settings = settings
        self._http_client: httpx.AsyncClient | None = None

    async def __aenter__(self):
        self._http_client = httpx.AsyncClient(timeout=self.settings.http_timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._http_client is not None:
            await self._http_client.aclose()

    def _select_ecb_client(self, is_local: bool) -> EcbClient:
        if is_local:
            local_ecb_settings: LocalEcbSettings = get_local_ecb_settings()
            raise NotImplementedError("Local ECB client not yet implemented")

        if self._http_client is None:
            raise RuntimeError("Container must be used as an async context manager when ECB Client is not local.")

        http_ecb_settings: HttpEcbSettings = get_http_ecb_settings()
        return HttpEcbClient(
            client=self._http_client,
            url=http_ecb_settings.url.unicode_string(),
            data_format=http_ecb_settings.format,
            observations=http_ecb_settings.observations,
        )

    def _select_archive_store(self, is_local: bool) -> ArchiveStore:
        pass

    def _select_rates_store(self, is_local: bool) -> RatesStore:
        pass

    def get_ingestion_service(self) -> IngestionService:
        return IngestionService(
            ecb_client=self._select_ecb_client(self.settings.is_local_ecb_client),
            archive_store=self._select_archive_store(self.settings.is_local_archive_store),
            rates_store=self._select_rates_store(self.settings.is_local_rates_store),
        )
