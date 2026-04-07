from pathlib import Path

from src.stores.vault.vault_store import VaultStore


class LocalVaultStore(VaultStore):
    def __init__(self, dir_path: Path) -> None:
        self.dir_path = dir_path

    def store(self, data: bytes, file_path: str) -> None:
        output_path: Path = self.dir_path / file_path
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "wb") as file:
            file.write(data)
