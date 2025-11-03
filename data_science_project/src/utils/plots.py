"""Visualization helpers for exploratory and explanatory graphics."""

from __future__ import annotations

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style='whitegrid')


def configure_figsize(width: float = 10, height: float = 6) -> None:
    """Apply a global default figure size for consistency."""
    plt.rcParams['figure.figsize'] = (width, height)


def histogram(series, *, bins: int = 30, title: str = '') -> plt.Axes:
    """Plot a histogram with seaborn defaults and return the axes."""
    ax = sns.histplot(series, bins=bins, kde=True)
    ax.set_title(title)
    return ax


def barplot(data, *, x: str, y: str, title: str = '', order=None) -> plt.Axes:
    """Create a barplot with labels and ordering control."""
    ax = sns.barplot(data=data, x=x, y=y, order=order)
    ax.set_title(title)
    return ax
