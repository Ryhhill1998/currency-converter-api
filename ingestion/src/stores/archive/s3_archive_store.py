from src.stores.archive.archive_store import ArchiveStore


class S3ArchiveStore(ArchiveStore):
    def __init__(self, client: "S3Client", bucket_name: str) -> None:
        self.client = client
        self.bucket_name = bucket_name

    def write(self) -> None:
        pass
