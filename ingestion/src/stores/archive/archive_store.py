from typing import Protocol, runtime_checkable


@runtime_checkable
class ArchiveStore(Protocol):
    def write(self) -> None:
        pass
