"""
app.py — Tech Stocks Dashboard
------------------------------
"""

import streamlit as st
import pandas as pd

import analytics
import plots
from data_loader import COMPANY_NAMES, TICKERS, apply_date_filter, load_stocks


# Page setup
st.set_page_config(
    page_title="Tech Stocks Dashboard",
    page_icon="📈",
    layout="wide",
)

#  CSS 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&family=Share+Tech+Mono&display=swap');

/* Background */
.stApp {
    background: radial-gradient(circle at top right, #0a192f, #020c1b);
    color: #e6f1ff;
}

/* Main title */
h1 {
    font-family: 'Orbitron', sans-serif !important;
    color: #00d4ff !important;
    font-size: 2.6rem !important;
    text-align: center;
    text-shadow: 0 0 20px rgba(0,212,255,0.5);
    margin-bottom: 4px !important;
}

/* Section headers */
h2, h3 {
    font-family: 'Rajdhani', sans-serif !important;
    color: #64ffda !important;
}

/* Metric cards */
div[data-testid="metric-container"] {
    background: rgba(10,25,47,0.7) !important;
    border: 1px solid rgba(0,212,255,0.15) !important;
    border-radius: 10px !important;
    padding: 16px !important;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}
div[data-testid="metric-container"]:hover {
    border: 1px solid #00d4ff !important;
    box-shadow: 0 0 20px rgba(0,212,255,0.2) !important;
}
div[data-testid="metric-container"] label {
    color: #8892b0 !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.85rem !important;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: #e6f1ff !important;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 1.1rem !important;
}

/* Dataframe */
div[data-testid="stDataFrame"] {
    border: 1px solid rgba(0,212,255,0.15) !important;
    border-radius: 10px !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(2,12,27,0.95) !important;
    border-right: 1px solid rgba(0,212,255,0.1) !important;
}
section[data-testid="stSidebar"] * {
    color: #e6f1ff !important;
}

/* Tabs */
div[data-testid="stTabs"] button {
    font-family: 'Rajdhani', sans-serif !important;
    color: #8892b0 !important;
    font-size: 0.95rem !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #00d4ff !important;
    border-bottom: 2px solid #00d4ff !important;
}

/* Divider */
hr { border-color: rgba(0,212,255,0.1) !important; }

/* Info / Warning boxes */
div[data-testid="stInfo"] {
    background: rgba(0,212,255,0.06) !important;
    border: 1px solid rgba(0,212,255,0.3) !important;
    border-radius: 8px !important;
    color: #e6f1ff !important;
}
div[data-testid="stWarning"] {
    background: rgba(255,166,0,0.06) !important;
    border: 1px solid rgba(255,166,0,0.3) !important;
    border-radius: 8px !important;
    color: #e6f1ff !important;
}

/* Conclusion card */
.conclusion-card {
    background: rgba(10,25,47,0.7);
    border: 1px solid rgba(0,212,255,0.15);
    border-radius: 12px;
    padding: 24px;
    margin: 12px 0;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}
.conclusion-card:hover {
    border: 1px solid #00d4ff;
    box-shadow: 0 0 25px rgba(0,212,255,0.2);
}
.conclusion-card .card-title {
    font-family: 'Rajdhani', sans-serif;
    color: #64ffda;
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 12px;
}
.conclusion-card .card-body {
    color: #e6f1ff;
    font-size: 1rem;
    line-height: 1.6;
}
.highlight-green {
    color: #00ff88;
    font-weight: bold;
    background: rgba(0,255,136,0.1);
    padding: 4px 10px;
    border-radius: 6px;
}
.highlight-red {
    color: #ff6b6b;
    font-weight: bold;
    background: rgba(255,107,107,0.1);
    padding: 4px 10px;
    border-radius: 6px;
}
.highlight-blue {
    color: #00d4ff;
    font-weight: bold;
    background: rgba(0,212,255,0.1);
    padding: 4px 10px;
    border-radius: 6px;
}

header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


#  Header
st.markdown("<h1>📈 TECH STOCKS DASHBOARD</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:#8892b0; font-family:Rajdhani,sans-serif; "
    "font-size:1.1rem; margin-bottom:32px;'>"
    "Stock performance analysis · Meta · Apple · Amazon · Netflix · Google · Microsoft · NVIDIA · "
    "July 2018 → July 2023</p>",
    unsafe_allow_html=True,
)


#  Load data
df = load_stocks()


# Sidebar 
st.sidebar.header("Filters")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

selected_stocks = st.sidebar.multiselect(
    "Select Stocks",
    options=TICKERS,
    default=TICKERS,
    format_func=lambda t: f"{t} — {COMPANY_NAMES[t]}",
)

st.sidebar.markdown("---")
st.sidebar.caption(f"📊 **{len(df):,}** trading days loaded")
st.sidebar.caption(f"📅 {min_date} → {max_date}")

st.sidebar.markdown("### Legend")
for ticker in TICKERS:
    color = plots.PALETTE[ticker]
    st.sidebar.markdown(
        f'<span style="color:{color}; font-weight:bold;">⬤</span> '
        f'{ticker} — {COMPANY_NAMES[ticker]}',
        unsafe_allow_html=True,
    )


# Apply filters
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

filtered = apply_date_filter(df, start_date, end_date)

if filtered.empty or not selected_stocks:
    st.warning("No data matches your filters. Try adjusting the date range or selecting stocks.")
    st.stop()


#  Tabs
tab_overview, tab_market, tab_analysis, tab_conclusion, tab_raw = st.tabs([
    "🏠 Overview",
    "📊 Market Share",
    "📈 Stock Analysis",
    "🏁 Conclusion",
    "📄 Raw Data",
])


# ══════════════════════════════════════════════════════════════
# TAB _ OVERVIEW
# ══════════════════════════════════════════════════════════════
with tab_overview:
    kpis = analytics.overview_kpis(filtered)
    mkt  = analytics.market_summary(filtered, selected_stocks)

    st.markdown("### Performance Summary")
    cols = st.columns(len(selected_stocks))
    for col, ticker in zip(cols, selected_stocks):
        if ticker not in kpis:
            continue
        k = kpis[ticker]
        col.metric(
            label=ticker,
            value=f"${k['last']:,.2f}",
            delta=f"{k['pct_change']:+.2f}%",
        )

    st.markdown("---")

    if mkt:
        c1, c2, c3 = st.columns(3)
        c1.metric("Best Performing Stock", mkt["best_company"],
                  f"{mkt['best_return']:+.2f}%")
        c2.metric("Worst Performing Stock", mkt["worst_company"],
                  f"{mkt['worst_return']:+.2f}%")
        c3.metric("Market Average Return", f"{mkt['avg_return']:+.2f}%")

    st.markdown("---")
    st.markdown("### Price History — All Stocks")
    st.pyplot(plots.line_all_stocks(filtered))

    st.markdown("---")
    st.markdown("### Summary Table")
    st.dataframe(analytics.summary_table(filtered),
                 use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════
# TAB _ MARKET SHARE
# ══════════════════════════════════════════════════════════════
with tab_market:
    st.markdown("### Market Share")
    st.caption("Portfolio weight of each stock based on its latest closing price.")

    kpis_filtered = {t: kpis[t] for t in selected_stocks if t in kpis}

    left, right = st.columns([2, 1])
    with left:
        st.pyplot(plots.pie_performance(kpis_filtered))
    with right:
        st.markdown("#### Numbers")
        rows = [
            {
                "Ticker":  t,
                "Company": COMPANY_NAMES[t],
                "Price":   f"${kpis_filtered[t]['last']:,.2f}",
                "Return":  f"{kpis_filtered[t]['pct_change']:+.2f}%",
            }
            for t in selected_stocks if t in kpis_filtered
        ]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════
# TAB _ STOCK ANALYSIS
# ══════════════════════════════════════════════════════════════
with tab_analysis:
    st.markdown("### Analyze a Single Stock")

    chosen = st.selectbox(
        "Choose a stock:",
        options=selected_stocks,
        format_func=lambda t: f"{t} — {COMPANY_NAMES[t]}",
    )

    if chosen:
        stats = analytics.stock_stats(filtered, chosen)

        c1, c2, c3, c4, c5, c6 = st.columns(6)
        c1.metric("Current Price", f"${stats['current']:,.2f}")
        c2.metric("Start Price",   f"${stats['start']:,.2f}")
        c3.metric("Total Return",  f"{stats['pct_change']:+.2f}%")
        c4.metric("All-Time High", f"${stats['max']:,.2f}")
        c5.metric("All-Time Low",  f"${stats['min']:,.2f}")
        c6.metric("Volatility",    f"{stats['volatility']:.2f}%")

        st.markdown("---")

        ma_window = st.slider("Moving Average Window (days)", 7, 90, 30)
        ma = analytics.moving_average(filtered, chosen, window=ma_window)
        st.pyplot(plots.line_single_stock(filtered, chosen, ma))

        st.markdown("---")

        best_m, worst_m = analytics.best_worst_months(filtered, chosen, n=3)
        left, right = st.columns(2)
        with left:
            st.markdown("#### Best 3 Months")
            st.dataframe(best_m, use_container_width=True, hide_index=True)
        with right:
            st.markdown("#### Worst 3 Months")
            st.dataframe(worst_m, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════
# TAB _ CONCLUSION
# ══════════════════════════════════════════════════════════════
with tab_conclusion:
    st.markdown("### Conclusion")

    conc = analytics.conclusion(filtered, selected_stocks)

    if conc:
        # Top metrics
        c1, c2, c3 = st.columns(3)
        c1.metric("Market Trend",        f"{conc['trend_emoji']} {conc['market_trend']}")
        c2.metric("Average Return",       f"{conc['avg_return']:+.2f}%")
        c3.metric("Best Stock",           conc["best_investment"],
                  f"{conc['best_return']:+.2f}%")

        st.markdown("---")

        # Four cards
        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown(f"""
            <div class="conclusion-card">
                <div class="card-title">🏆 Best Performing Stock</div>
                <div class="card-body">
                    <span class="highlight-green">{conc['best_investment']} &nbsp;
                    {conc['best_return']:+.2f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="conclusion-card">
                <div class="card-title">🛡️ Lowest Risk Stock</div>
                <div class="card-body">
                    <span class="highlight-blue">{conc['safest_stock']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            st.markdown(f"""
            <div class="conclusion-card">
                <div class="card-title">📉 Worst Performing Stock</div>
                <div class="card-body">
                    <span class="highlight-red">{conc['worst_investment']} &nbsp;
                    {conc['worst_return']:+.2f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="conclusion-card">
                <div class="card-title">⚠️ Highest Risk Stock</div>
                <div class="card-body">
                    <span class="highlight-red">{conc['riskiest_stock']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Final analysis card
        st.markdown(f"""
        <div class="conclusion-card">
            <div class="card-title">📊 Final Analysis</div>
            <div class="card-body">{conc['analysis_text']}</div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# TAB _ RAW DATA
# ══════════════════════════════════════════════════════════════
with tab_raw:
    st.markdown(f"### Raw Data — {len(filtered):,} rows")

    cols_to_show = ["Date"] + [t for t in selected_stocks if t in filtered.columns]
    display_df = filtered[cols_to_show].copy()
    display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.download_button(
        label="Download CSV",
        data=display_df.to_csv(index=False).encode("utf-8"),
        file_name="tech_stocks_filtered.csv",
        mime="text/csv",
    )   
# Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align:center; color:#8892b0; font-size:0.85rem; "
        "font-family:Rajdhani,sans-serif;'>"
        """
 I would like to extend my sincere thanks to my team members who contributed to making this project a success.
Team Members:

Mustafa Ali Darwish (myself)\n\n
Abdullah Mabrouk Abdelaziz\n\n
Eslam Mohamed Zakaria\n\n
Mohamed Ahmed Shaaban\n\n
Abdelrahman Rabie Khalil\n\n""" 
        "</p>",
        unsafe_allow_html=True,
    )

    
    

