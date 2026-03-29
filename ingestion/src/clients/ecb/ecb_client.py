from typing import Protocol, runtime_checkable


@runtime_checkable
class EcbClient(Protocol):
    async def fetch_latest_rates(self) -> bytes:
        pass
