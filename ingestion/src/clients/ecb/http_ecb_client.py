import httpx

from src.clients.ecb.ecb_client import EcbClient


class HttpEcbClient(EcbClient):
    def __init__(
        self, client: httpx.Client, url: str, data_format: str, observations: int
    ) -> None:
        self.client = client
        self.url = url
        self.observations = observations
        self.data_format = data_format
        self._params: dict[str, str | int] = {
            "format": self.data_format,
            "lastNObservations": self.observations,
            "detail": "dataonly",
        }

    def fetch_latest_rates(self) -> bytes:
        response = self.client.get(
            url=self.url, params=self._params, follow_redirects=True
        )
        response.raise_for_status()
        return response.read()
