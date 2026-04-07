import io

import polars as pl

def parse_ecb_rates(raw_content: bytes) -> list[dict]:
    return (
        pl.read_csv(io.BytesIO(raw_content))
    ).to_dicts()
