from src.stores.rates.rates_store import RatesStore


class S3RatesStore(RatesStore):
    def __init__(self, client: "S3Client", bucket_name: str) -> None:
        self.client = client
        self.bucket_name = bucket_name

    def write(self) -> None:
        pass
