import httpx

from src.clients.ecb.ecb_client import EcbClient
from src.clients.ecb.http_ecb_client import HttpEcbClient
from src.models.settings import GeneralSettings, get_general_settings, LocalEcbSettings, get_local_ecb_settings, \
    HttpEcbSettings, get_http_ecb_settings
from src.services.ingestion_service import IngestionService
from src.stores.archive.archive_store import ArchiveStore
from src.stores.rates.rates_store import RatesStore

client = httpx.AsyncClient()


async def handler(_, __) -> dict[str, str]:
    settings: GeneralSettings = get_general_settings()

    ecb_client: EcbClient = select_ecb_client(settings.is_local_ecb_client)
    archive_store: ArchiveStore = select_archive_store(settings.is_local_archive_store)
    rates_store: RatesStore = select_rates_store(settings.is_local_rates_store)

    ingestion_service = IngestionService(ecb_client=ecb_client, archive_store=archive_store, rates_store=rates_store)

    await ingestion_service.run()

    return {"status": "success"}
