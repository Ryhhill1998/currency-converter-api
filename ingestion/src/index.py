from src.container import Container
from src.models.settings import GeneralSettings, get_general_settings

settings: GeneralSettings = get_general_settings()


async def handler(_, __) -> dict[str, str]:
    async with Container(settings) as container:
        ingestion_service = container.get_ingestion_service()
        await ingestion_service.run()

    return {"status": "success"}
