from datetime import datetime

from src.containers.ingestion_service_container import IngestionServiceContainer
from src.models.settings import Settings, get_settings


def handler(_, __, settings: Settings | None = None) -> dict[str, str]:
    system_run_timestamp: datetime = datetime.now()
    app_settings: Settings = settings or get_settings()

    with IngestionServiceContainer(app_settings) as ingestion_service_container:
        ingestion_service = ingestion_service_container.get_ingestion_service()
        ingestion_service.run(system_run_timestamp)

    return {"status": "success"}
