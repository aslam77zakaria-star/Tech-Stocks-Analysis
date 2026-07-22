"""
data_loader.py
--------------
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

DATA_FILE = Path(__file__).parent / "tech_stocks.csv"

COMPANY_NAMES = {
    "META":  "Meta Platforms",
    "AAPL":  "Apple",
    "AMZN":  "Amazon",
    "NFLX":  "Netflix",
    "GOOGL": "Google",
    "MSFT":  "Microsoft",
    "NVDA":  "NVIDIA",
}

TICKERS = list(COMPANY_NAMES.keys())


@st.cache_data(show_spinner="Loading stock data...")
def load_stocks(path: Path | str = DATA_FILE) -> pd.DataFrame:
    """Read the CSV and return a cleaned DataFrame.

    Cleaning steps:
    1. Parse Date as a real datetime.
    2. Drop rows missing critical fields.
    3. Add helper columns Year and Month.
    """
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"]).copy()
    df["Year"]  = df["Date"].dt.year
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    df = df.sort_values("Date").reset_index(drop=True)
    return df


def apply_date_filter(
    df: pd.DataFrame,
    start_date,
    end_date,
) -> pd.DataFrame:
    """Return only rows within the chosen date range."""
    start = pd.to_datetime(start_date)
    end   = pd.to_datetime(end_date)
    return df[(df["Date"] >= start) & (df["Date"] <= end)].copy()
