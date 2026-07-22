"""
plots.py
--------
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

from data_loader import COMPANY_NAMES, TICKERS

PALETTE = {
    "META":  "#1877F2",
    "AAPL":  "#888888",
    "AMZN":  "#FF9900",
    "NFLX":  "#E50914",
    "GOOGL": "#34A853",
    "MSFT":  "#00A4EF",
    "NVDA":  "#76B900",
}

STYLE = {
    "bg":    "#0E1117",
    "fg":    "#FAFAFA",
    "grid":  "#2A2A3A",
    "ax_bg": "#1A1A2E",
}


def _apply_dark_style(fig, axes):
    fig.patch.set_facecolor(STYLE["bg"])
    ax_list = axes if hasattr(axes, "__iter__") else [axes]
    for ax in ax_list:
        ax.set_facecolor(STYLE["ax_bg"])
        ax.tick_params(colors=STYLE["fg"], labelsize=9)
        ax.xaxis.label.set_color(STYLE["fg"])
        ax.yaxis.label.set_color(STYLE["fg"])
        ax.title.set_color(STYLE["fg"])
        for spine in ax.spines.values():
            spine.set_edgecolor(STYLE["grid"])
        ax.grid(True, linestyle="--", alpha=0.3, color=STYLE["grid"])


# ── 1. All-stocks line chart (Overview) ───────────────────────────────────────
def line_all_stocks(df: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 4))
    if df.empty:
        ax.text(0.5, 0.5, "No data", ha="center", va="center", color=STYLE["fg"])
        _apply_dark_style(fig, ax)
        return fig

    for ticker in TICKERS:
        if ticker in df.columns:
            ax.plot(df["Date"], df[ticker],
                    label=ticker, color=PALETTE[ticker], linewidth=1.5)

    ax.set_title("Stock Price History — All Companies", fontsize=13, fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend(loc="upper left", fontsize=8,
              facecolor=STYLE["ax_bg"], labelcolor=STYLE["fg"], framealpha=0.7)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    _apply_dark_style(fig, ax)
    fig.tight_layout()
    return fig


# ── 2. Single stock + moving average (Stock Analysis) ────────────────────────
def line_single_stock(df: pd.DataFrame, ticker: str, ma: pd.Series) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 4))
    if df.empty or ticker not in df.columns:
        ax.text(0.5, 0.5, "No data", ha="center", va="center", color=STYLE["fg"])
        _apply_dark_style(fig, ax)
        return fig

    company = COMPANY_NAMES.get(ticker, ticker)
    ax.plot(df["Date"], df[ticker],
            color=PALETTE[ticker], linewidth=1.5, label=f"{ticker} Price")
    if ma is not None and not ma.empty:
        ax.plot(df["Date"], ma,
                color="#FFD700", linewidth=1.5, linestyle="--",
                label="Moving Average", alpha=0.9)

    ax.set_title(f"{company} ({ticker}) — Price History", fontsize=13, fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend(facecolor=STYLE["ax_bg"], labelcolor=STYLE["fg"], framealpha=0.7)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    _apply_dark_style(fig, ax)
    fig.tight_layout()
    return fig


# ── 3. Pie chart (Market Share tab) ──────────────────────────────────────────
def pie_performance(kpis: dict) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(7, 7))
    if not kpis:
        ax.text(0.5, 0.5, "No data", ha="center", va="center", color=STYLE["fg"])
        _apply_dark_style(fig, ax)
        return fig

    tickers = list(kpis.keys())
    values  = [kpis[t]["last"] for t in tickers]
    colors  = [PALETTE.get(t, "#AAAAAA") for t in tickers]

    wedges, texts, autotexts = ax.pie(
        values, labels=tickers, autopct="%1.1f%%",
        colors=colors, startangle=90, pctdistance=0.75,
    )
    for text in texts:
        text.set_color(STYLE["fg"])
        text.set_fontsize(11)
    for at in autotexts:
        at.set_color("white")
        at.set_fontsize(9)

    ax.set_title("Portfolio Weight by Price", fontsize=13, fontweight="bold",
                 color=STYLE["fg"])
    fig.patch.set_facecolor(STYLE["bg"])
    fig.tight_layout()
    return fig
