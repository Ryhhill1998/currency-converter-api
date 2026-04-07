from src.stores.archive.archive_store import ArchiveStore


class LocalArchiveStore(ArchiveStore):
    def __init__(self, dir_path: str) -> None:
        self.dir_path = dir_path

    def write(self, data: bytes, file_path: str) -> None:
        pass
