from src.containers.ingestion_service_container import IngestionServiceContainer
from src.models.settings import GeneralSettings, get_general_settings


async def handler(_, __) -> dict[str, str]:
    settings: GeneralSettings = get_general_settings()

    async with IngestionServiceContainer(settings) as container:
        ingestion_service = container.get_ingestion_service()
        await ingestion_service.run()

    return {"status": "success"}
