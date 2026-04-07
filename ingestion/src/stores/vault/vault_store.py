from typing import Protocol, runtime_checkable


@runtime_checkable
class VaultStore(Protocol):
    def store(self, data: bytes, file_path: str) -> None:
        pass
