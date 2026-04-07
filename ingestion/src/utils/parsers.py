import io
import json

import polars as pl

def parse_raw_rates(raw_content: bytes) -> list[dict]:
    return (
        pl.read_csv(io.BytesIO(raw_content))
    ).to_dicts()


def serialise_rates(rates: list[dict]) -> bytes:
    return json.dumps(rates).encode("utf-8")
