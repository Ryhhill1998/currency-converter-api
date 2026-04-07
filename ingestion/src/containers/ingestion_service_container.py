from typing import Self

import boto3
import httpx
from mypy_boto3_s3.client import S3Client

from src.clients.ecb.ecb_client import EcbClient
from src.clients.ecb.http_ecb_client import HttpEcbClient
from src.clients.ecb.local_ecb_client import LocalEcbClient
from src.models.settings import Settings
from src.services.ingestion_service import IngestionService
from src.stores.vault.vault_store import VaultStore
from src.stores.vault.local_vault_store import LocalVaultStore
from src.stores.vault.s3_vault_store import S3VaultStore
from src.stores.live.live_store import LiveStore


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

    def _select_vault_store(self, is_local: bool) -> VaultStore:
        if is_local:
            return LocalVaultStore(self.settings.local_archive_dir_path)

        s3_client: "S3Client" = boto3.client("s3")
        return S3VaultStore(client=s3_client, bucket_name=self.settings.s3_archive_bucket_name)

    def _select_live_store(self, is_local: bool) -> LiveStore:
        pass

    def get_ingestion_service(self) -> IngestionService:
        self._ensure_context()

        return IngestionService(
            ecb_client=self._select_ecb_client(self.settings.is_local_ecb_client),
            vault_store=self._select_vault_store(self.settings.is_local_vault_store),
            live_store=self._select_live_store(self.settings.is_local_live_store),
        )
