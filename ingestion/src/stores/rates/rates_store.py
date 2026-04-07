from typing import Protocol, runtime_checkable


@runtime_checkable
class RatesStore(Protocol):
    def write(self, rates_map: list[dict]) -> None:
        pass
