from src.clients.ecb.ecb_client import EcbClient


class LocalEcbClient(EcbClient):
    async def fetch_latest_rates(self) -> bytes:
        pass
