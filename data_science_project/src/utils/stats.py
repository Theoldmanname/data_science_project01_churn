"""Statistical helper functions shared across notebooks."""

from __future__ import annotations

from typing import Iterable, Tuple

import numpy as np
import pandas as pd
from scipy import stats


def summarize_numeric(series: pd.Series) -> pd.Series:
    """Return a descriptive statistics summary for a numeric series."""
    return series.agg(['count', 'mean', 'std', 'min', 'median', 'max'])


def cramers_v(confusion_matrix: pd.DataFrame) -> float:
    """Compute Cramer's V statistic for categorical association."""
    chi2 = stats.chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.to_numpy().sum()
    r, k = confusion_matrix.shape
    return np.sqrt((chi2 / n) / (min(k - 1, r - 1)))


def confidence_interval(data: Iterable[float], confidence: float = 0.95) -> Tuple[float, float]:
    """Calculate a confidence interval for the mean of numeric data."""
    array = np.array(list(data))
    mean = array.mean()
    sem = stats.sem(array)
    margin = sem * stats.t.ppf((1 + confidence) / 2.0, len(array) - 1)
    return mean - margin, mean + margin
