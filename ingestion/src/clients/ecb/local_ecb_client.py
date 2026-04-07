from src.clients.ecb.ecb_client import EcbClient


class LocalEcbClient(EcbClient):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def fetch_latest_rates(self) -> bytes:
        pass
