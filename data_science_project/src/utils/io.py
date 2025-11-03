"""IO utilities for data ingestion and persistence."""

from pathlib import Path
from typing import Optional

import pandas as pd


def load_csv(path: Path, *, dtype: Optional[dict] = None, parse_dates: Optional[list] = None) -> pd.DataFrame:
    """Load a CSV file with optional dtype and date parsing configuration."""
    return pd.read_csv(path, dtype=dtype, parse_dates=parse_dates)


def save_dataframe(df: pd.DataFrame, path: Path, *, index: bool = False) -> None:
    """Persist a DataFrame to CSV with consistent options."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=index)
