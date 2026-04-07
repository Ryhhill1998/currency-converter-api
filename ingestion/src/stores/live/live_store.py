from typing import Protocol, runtime_checkable


@runtime_checkable
class LiveStore(Protocol):
    def store(self, rates_map: dict[str, dict]) -> None:
        pass
