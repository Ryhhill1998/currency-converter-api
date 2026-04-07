from mypy_boto3_s3.client import S3Client

from src.stores.live.live_store import LiveStore


class S3LiveStore(LiveStore):
    def __init__(self, client: "S3Client", bucket_name: str) -> None:
        self.client = client
        self.bucket_name = bucket_name

    def store(self, rates_map: dict[str, dict]) -> None:
        pass
