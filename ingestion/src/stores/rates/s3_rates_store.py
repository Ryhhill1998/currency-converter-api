from mypy_boto3_s3.client import S3Client

from src.stores.rates.rates_store import RatesStore


class S3RatesStore(RatesStore):
    def __init__(self, client: "S3Client", bucket_name: str) -> None:
        self.client = client
        self.bucket_name = bucket_name

    def write(self, rates_map: list[dict]) -> None:
        pass
