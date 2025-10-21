import os, sys
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
# Ensure repo root is on sys.path so we can import branding/style_utils.py
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from branding.style_utils import inject_css, banner, set_altair_theme, COLORS

# Apply unified branding
inject_css()
set_altair_theme()
banner(
    title="Promo Impact Forecaster",
    subtitle="Forecast revenue, conversion, and contribution margin under different discount scenarios.",
    emoji="📈"
)
st.markdown(
"""
Model how discount depth impacts **conversion, AOV, revenue, and contribution margin**.
- Adjust inputs in the sidebar
- Review the scenario table
- Explore the charts
- Download the CSV for planning decks
"""
)

# -------------------------
# Sidebar: Assumptions
# -------------------------
st.sidebar.header("Assumptions")

traffic = st.sidebar.number_input("Sessions (traffic)", min_value=1000, value=100_000, step=1000)
base_conv = st.sidebar.number_input("Baseline conversion rate", min_value=0.0001, max_value=1.0, value=0.025, step=0.001, format="%.4f")
base_price = st.sidebar.number_input("List price ($)", min_value=1.0, value=80.0, step=1.0)
unit_cost = st.sidebar.number_input("Unit cost ($)", min_value=0.0, value=32.0, step=1.0)
elasticity = st.sidebar.number_input("Elasticity (conv lift per 100% disc.)", min_value=0.1, value=1.8, step=0.1)
avg_qty = st.sidebar.number_input("Avg units per order", min_value=0.1, value=1.3, step=0.1)
max_conv_cap = st.sidebar.number_input("Cap conversion (safety)", min_value=0.01, max_value=1.0, value=0.25, step=0.01)

discount_min = st.sidebar.slider("Min discount (%)", 0, 80, 0)
discount_max = st.sidebar.slider("Max discount (%)", 5, 90, 40)
discount_step = st.sidebar.slider("Step (%)", 1, 20, 5)

# -------------------------
# Optional: upload historical transactions (context only)
# -------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("Optional: Upload sample transactions")
uploaded = st.sidebar.file_uploader("CSV with columns: date, qty (optional)", type=["csv"])

if uploaded is not None:
    try:
        hist = pd.read_csv(uploaded)
        st.sidebar.success("Transactions loaded")
    except Exception as e:
        hist = None
        st.sidebar.error(f"Could not read CSV: {e}")
else:
    hist = None

# -------------------------
# Scenario builder
# -------------------------
def build_scenarios(traffic, base_conv, base_price, unit_cost, elasticity, avg_qty, max_conv_cap,
                    d_min, d_max, d_step):
    grid = np.arange(d_min/100, d_max/100 + 0.0001, d_step/100)
    rows = []
    for d in grid:
        conv = min(base_conv * (1 + elasticity * d), max_conv_cap)
        price_after = base_price * (1 - d)
        aov = price_after * avg_qty

        orders = traffic * conv
        revenue = orders * aov

        cogs_per_order = unit_cost * avg_qty
        margin_per_order = (price_after * avg_qty) - cogs_per_order
        contrib_margin = orders * margin_per_order

        rows.append({
            "discount_rate_%": round(d*100, 1),
            "conversion_rate": round(conv, 4),
            "orders": int(round(orders)),
            "AOV": round(aov, 2),
            "revenue": round(revenue, 2),
            "contribution_margin": round(contrib_margin, 2),
            "revenue_per_session": round(revenue / traffic, 2),
            "cm_per_session": round(contrib_margin / traffic, 2)
        })
    return pd.DataFrame(rows)

scenarios = build_scenarios(
    traffic, base_conv, base_price, unit_cost, elasticity, avg_qty, max_conv_cap,
    discount_min, discount_max, discount_step
)

# -------------------------
# Summary KPIs
# -------------------------
c1, c2, c3, c4 = st.columns(4)
best_rev = scenarios.loc[scenarios["revenue"].idxmax()]
best_cm = scenarios.loc[scenarios["contribution_margin"].idxmax()]

c1.metric("Max Revenue ($)", f"{best_rev['revenue']:,.0f}", help=f"@ {best_rev['discount_rate_%']}% discount")
c2.metric("Max Contribution ($)", f"{best_cm['contribution_margin']:,.0f}", help=f"@ {best_cm['discount_rate_%']}% discount")
c3.metric("Orders (max revenue)", f"{int(best_rev['orders']):,}")
c4.metric("AOV (max revenue)", f"${best_rev['AOV']:,.2f}")

st.markdown("### Scenario Table")
st.dataframe(scenarios, use_container_width=True)

# -------------------------
# Charts
# -------------------------
left, right = st.columns(2)

with left:
    st.markdown("#### Revenue by Discount")
    chart_rev = alt.Chart(scenarios).mark_line(point=True).encode(
        x=alt.X("discount_rate_%:Q", title="Discount (%)"),
        y=alt.Y("revenue:Q", title="Revenue"),
        tooltip=list(scenarios.columns)
    ).properties(height=320)
    st.altair_chart(chart_rev, use_container_width=True)

with right:
    st.markdown("#### Contribution Margin by Discount")
    chart_cm = alt.Chart(scenarios).mark_line(point=True).encode(
        x=alt.X("discount_rate_%:Q", title="Discount (%)"),
        y=alt.Y("contribution_margin:Q", title="Contribution Margin"),
        tooltip=list(scenarios.columns)
    ).properties(height=320)
    st.altair_chart(chart_cm, use_container_width=True)

st.markdown("#### Conversion & AOV")
chart_ca = alt.Chart(scenarios).transform_fold(
    ["conversion_rate", "AOV"], as_=["metric", "value"]
).mark_line(point=True).encode(
    x=alt.X("discount_rate_%:Q", title="Discount (%)"),
    y=alt.Y("value:Q", title="Value"),
    color="metric:N",
    tooltip=list(scenarios.columns)
).properties(height=320)
st.altair_chart(chart_ca, use_container_width=True)

# -------------------------
# Download
# -------------------------
st.markdown("### Download Scenarios CSV")
st.download_button(
    "⬇️ Download scenarios.csv",
    data=scenarios.to_csv(index=False),
    file_name="promo_scenarios.csv",
    mime="text/csv"
)

# -------------------------
# Optional context: show simple aggregates if a transactions CSV was uploaded
# -------------------------
if hist is not None and not hist.empty:
    st.markdown("### Uploaded Transactions (Context)")
    if "qty" in hist.columns:
        total_units = int(hist["qty"].sum())
        st.write(f"Total units in file: **{total_units:,}**")
    st.dataframe(hist.head(20), use_container_width=True)

st.caption("Tip: tune elasticity and caps based on historical test results by category/segment.")
