from typing import Self

import boto3
import httpx
from mypy_boto3_s3.client import S3Client

from src.clients.ecb.ecb_client import EcbClient
from src.clients.ecb.http_ecb_client import HttpEcbClient
from src.clients.ecb.local_ecb_client import LocalEcbClient
from src.models.settings import Settings
from src.services.ingestion_service import IngestionService
from src.stores.archive.archive_store import ArchiveStore
from src.stores.archive.local_archive_store import LocalArchiveStore
from src.stores.archive.s3_archive_store import S3ArchiveStore
from src.stores.rates.rates_store import RatesStore


class IngestionServiceContainer:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._http_client: httpx.Client | None = None
        self._is_entered: bool = False

    def __enter__(self) -> Self:
        self._is_entered = True

        if not self.settings.is_local_ecb_client:
            self._http_client = httpx.Client(timeout=self.settings.http_timeout)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._http_client is not None:
            self._http_client.close()

        self._is_entered = False

    def _ensure_context(self) -> None:
        if not self._is_entered:
            raise RuntimeError(
                "IngestionServiceContainer must be used as a context manager. "
                "Example: with IngestionServiceContainer(settings) as container:"
            )

    def _select_ecb_client(self, is_local: bool) -> EcbClient:
        if is_local:
            return LocalEcbClient(self.settings.local_ecb_file_path)

        assert self._http_client is not None

        return HttpEcbClient(
            client=self._http_client,
            url=self.settings.http_ecb_url.unicode_string(),
            data_format=self.settings.http_ecb_format,
            observations=self.settings.http_ecb_observations,
        )

    def _select_archive_store(self, is_local: bool) -> ArchiveStore:
        if is_local:
            return LocalArchiveStore(self.settings.local_archive_dir_path)

        s3_client: "S3Client" = boto3.client("s3")
        return S3ArchiveStore(client=s3_client, bucket_name=self.settings.s3_archive_bucket_name)

    def _select_rates_store(self, is_local: bool) -> RatesStore:
        pass

    def get_ingestion_service(self) -> IngestionService:
        self._ensure_context()

        return IngestionService(
            ecb_client=self._select_ecb_client(self.settings.is_local_ecb_client),
            archive_store=self._select_archive_store(self.settings.is_local_archive_store),
            rates_store=self._select_rates_store(self.settings.is_local_rates_store),
        )
