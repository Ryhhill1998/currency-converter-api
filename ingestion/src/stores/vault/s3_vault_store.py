from mypy_boto3_s3.client import S3Client

from src.stores.vault.vault_store import VaultStore


class S3VaultStore(VaultStore):
    def __init__(self, client: "S3Client", bucket_name: str) -> None:
        self.client = client
        self.bucket_name = bucket_name

    def store(self, data: bytes, file_path: str) -> None:
        self.client.put_object(Bucket=self.bucket_name, Key=file_path, Body=data)
