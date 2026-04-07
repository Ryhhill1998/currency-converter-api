from pathlib import Path

from src.stores.archive.archive_store import ArchiveStore


class LocalArchiveStore(ArchiveStore):
    def __init__(self, dir_path: Path) -> None:
        self.dir_path = dir_path

    def write(self, data: bytes, file_path: str) -> None:
        self.dir_path.mkdir(parents=True, exist_ok=True)
        output_path: Path = self.dir_path / file_path

        with open(output_path, "wb") as file:
            file.write(data)
