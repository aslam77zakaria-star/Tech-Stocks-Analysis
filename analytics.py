"""
analytics.py
------------
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from data_loader import TICKERS


def overview_kpis(df: pd.DataFrame) -> dict:
    """Return headline KPI numbers for the Overview tab."""
    if df.empty:
        return {}

    kpis = {}
    for ticker in TICKERS:
        if ticker not in df.columns:
            continue
        first_price = df[ticker].iloc[0]
        last_price  = df[ticker].iloc[-1]
        pct_change  = ((last_price - first_price) / first_price) * 100
        kpis[ticker] = {
            "first":      round(first_price, 2),
            "last":       round(last_price, 2),
            "pct_change": round(pct_change, 2),
            "max":        round(df[ticker].max(), 2),
            "min":        round(df[ticker].min(), 2),
        }
    return kpis


def market_summary(df: pd.DataFrame, tickers: list[str]) -> dict:
    """Return best stock, worst stock, and market average return."""
    if df.empty:
        return {}

    from data_loader import COMPANY_NAMES
    returns = {}
    for ticker in tickers:
        if ticker not in df.columns:
            continue
        first = df[ticker].iloc[0]
        last  = df[ticker].iloc[-1]
        returns[ticker] = round(((last - first) / first) * 100, 2)

    if not returns:
        return {}

    best_ticker  = max(returns, key=returns.get)
    worst_ticker = min(returns, key=returns.get)
    avg_return   = round(sum(returns.values()) / len(returns), 2)

    return {
        "best_ticker":   best_ticker,
        "best_company":  COMPANY_NAMES[best_ticker],
        "best_return":   returns[best_ticker],
        "worst_ticker":  worst_ticker,
        "worst_company": COMPANY_NAMES[worst_ticker],
        "worst_return":  returns[worst_ticker],
        "avg_return":    avg_return,
    }


def summary_table(df: pd.DataFrame) -> pd.DataFrame:
    """Return a summary table with first price, last price, change% for all stocks."""
    if df.empty:
        return pd.DataFrame()

    rows = []
    for ticker in TICKERS:
        if ticker not in df.columns:
            continue
        from data_loader import COMPANY_NAMES
        first = df[ticker].iloc[0]
        last  = df[ticker].iloc[-1]
        pct   = ((last - first) / first) * 100
        rows.append({
            "Ticker":       ticker,
            "Company":      COMPANY_NAMES[ticker],
            "Start Price":  f"${first:,.2f}",
            "End Price":    f"${last:,.2f}",
            "Total Return": f"{pct:+.2f}%",
            "Max Price":    f"${df[ticker].max():,.2f}",
            "Min Price":    f"${df[ticker].min():,.2f}",
        })
    return pd.DataFrame(rows)


def stock_stats(df: pd.DataFrame, ticker: str) -> dict:
    """Return stats for a single stock."""
    if df.empty or ticker not in df.columns:
        return {}
    s = df[ticker]
    first = s.iloc[0]
    last  = s.iloc[-1]
    return {
        "current":    round(last, 2),
        "start":      round(first, 2),
        "pct_change": round(((last - first) / first) * 100, 2),
        "max":        round(s.max(), 2),
        "min":        round(s.min(), 2),
        "avg":        round(s.mean(), 2),
        "volatility": round(s.pct_change().std() * np.sqrt(252) * 100, 2),
    }


def moving_average(df: pd.DataFrame, ticker: str, window: int = 30) -> pd.Series:
    """Return the rolling moving average for a ticker."""
    if ticker not in df.columns:
        return pd.Series(dtype=float)
    return df[ticker].rolling(window=window).mean()


def best_worst_months(df: pd.DataFrame, ticker: str, n: int = 3) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return best and worst n months for a ticker by monthly return."""
    if ticker not in df.columns:
        return pd.DataFrame(), pd.DataFrame()

    temp = df[["Date", ticker]].copy()
    temp["Month"] = temp["Date"].dt.to_period("M").astype(str)

    monthly = (
        temp.groupby("Month")[ticker]
        .agg(["first", "last"])
        .reset_index()
    )
    monthly["Return (%)"] = ((monthly["last"] - monthly["first"]) / monthly["first"] * 100).round(2)
    monthly = monthly.rename(columns={"first": "Start Price ($)", "last": "End Price ($)"})
    monthly["Start Price ($)"] = monthly["Start Price ($)"].round(2)
    monthly["End Price ($)"]   = monthly["End Price ($)"].round(2)

    best  = monthly.nlargest(n,  "Return (%)")
    worst = monthly.nsmallest(n, "Return (%)")
    return best, worst


def conclusion(df: pd.DataFrame, tickers: list[str]) -> dict:
    """Generate conclusion using np.polyfit for smarter trend detection."""
    if df.empty:
        return {}

    from data_loader import COMPANY_NAMES
    returns      = {}
    volatilities = {}

    for ticker in tickers:
        if ticker not in df.columns:
            continue
        s = df[ticker]
        returns[ticker]      = ((s.iloc[-1] / s.iloc[0]) - 1) * 100
        volatilities[ticker] = s.pct_change().std() * np.sqrt(252) * 100

    if not returns:
        return {}

    # ── Market trend via np.polyfit (smarter than just avg) ──────────────────
    # حساب متوسط السوق يومياً
    available = [t for t in tickers if t in df.columns]
    market_index = df[available].mean(axis=1)

    # np.polyfit بيرسم خط على السعر ويحسب ميله
    # لو الميل موجب = السوق طالع، لو سالب = نازل
    trend_slope = np.polyfit(range(len(market_index)), market_index, 1)[0]

    if trend_slope > 0:
        market_trend = "Bullish (Up)"
        trend_emoji  = "📈"
    else:
        market_trend = "Bearish (Down)"
        trend_emoji  = "📉"

    avg_return = sum(returns.values()) / len(returns)
    best_t     = max(returns,      key=returns.get)
    worst_t    = min(returns,      key=returns.get)
    safest_t   = min(volatilities, key=volatilities.get)
    riskiest_t = max(volatilities, key=volatilities.get)

    analysis_text = (
        f"The market during this period is showing {market_trend} {trend_emoji}."
        f"Average market return: {avg_return:+.2f}%. \n\n"
        f"The best performing stock is {COMPANY_NAMES[best_t]} ({best_t}) "
        f"with a {returns[best_t]:+.2f}% return.\n\n"
        f"The lowest risk stock is {COMPANY_NAMES[safest_t]} ({safest_t}) \n\n"
        f"based on price volatility."
    )

    return {
        "best_investment":  f"{COMPANY_NAMES[best_t]} ({best_t})",
        "best_return":      round(returns[best_t], 2),
        "worst_investment": f"{COMPANY_NAMES[worst_t]} ({worst_t})",
        "worst_return":     round(returns[worst_t], 2),
        "market_trend":     market_trend,
        "trend_emoji":      trend_emoji,
        "avg_return":       round(avg_return, 2),
        "safest_stock":     f"{COMPANY_NAMES[safest_t]} ({safest_t})",
        "riskiest_stock":   f"{COMPANY_NAMES[riskiest_t]} ({riskiest_t})",
        "analysis_text":    analysis_text,
     }