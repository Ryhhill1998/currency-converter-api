from typing import Protocol, runtime_checkable


@runtime_checkable
class EcbClient(Protocol):
    def fetch_latest_rates(self) -> bytes:
        pass
