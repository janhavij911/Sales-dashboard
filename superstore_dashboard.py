"""
superstore_dashboard.py
An interactive Superstore Sales Dashboard built with Streamlit and Plotly.
Replicates the classic "Sample Superstore" analysis: sales trends, product
performance, shipping analysis, and regional analysis, with sidebar filters.

Run:
    streamlit run superstore_dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Superstore Sales Dashboard", page_icon="📊", layout="wide")

# ---------------------------------------------------------------------------
# Generate a realistic sample Superstore-style dataset (self-contained, no
# external file or download dependency needed)
# ---------------------------------------------------------------------------

@st.cache_data
def load_data(n_rows: int = 2000) -> pd.DataFrame:
    np.random.seed(42)

    categories = {
        "Furniture": ["Chairs", "Tables", "Bookcases", "Furnishings"],
        "Office Supplies": ["Binders", "Paper", "Storage", "Art", "Labels"],
        "Technology": ["Phones", "Accessories", "Machines", "Copiers"],
    }
    regions = ["East", "West", "Central", "South"]
    states_by_region = {
        "East": ["New York", "Pennsylvania", "New Jersey"],
        "West": ["California", "Washington", "Oregon"],
        "Central": ["Texas", "Illinois", "Ohio"],
        "South": ["Florida", "Georgia", "North Carolina"],
    }
    ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]
    segments = ["Consumer", "Corporate", "Home Office"]

    rows = []
    date_range = pd.date_range("2022-01-01", "2024-12-31", freq="D")

    for i in range(n_rows):
        category = np.random.choice(list(categories.keys()), p=[0.25, 0.45, 0.30])
        sub_category = np.random.choice(categories[category])
        region = np.random.choice(regions)
        state = np.random.choice(states_by_region[region])
        order_date = np.random.choice(date_range)

        base_sales = {"Furniture": 350, "Office Supplies": 60, "Technology": 450}[category]
        sales = max(5, np.random.gamma(2, base_sales / 2))
        discount = np.random.choice([0, 0.1, 0.2, 0.3], p=[0.4, 0.3, 0.2, 0.1])
        profit_margin = np.random.uniform(-0.15, 0.35)
        profit = sales * profit_margin
        quantity = np.random.randint(1, 10)

        rows.append({
            "Order Date": pd.Timestamp(order_date),
            "Category": category,
            "Sub-Category": sub_category,
            "Region": region,
            "State": state,
            "Segment": np.random.choice(segments),
            "Ship Mode": np.random.choice(ship_modes, p=[0.6, 0.2, 0.15, 0.05]),
            "Sales": round(sales, 2),
            "Profit": round(profit, 2),
            "Quantity": quantity,
            "Discount": discount,
        })

    return pd.DataFrame(rows)


df = load_data()

# ---------------------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------------------

st.sidebar.header("🔍 Filters")

date_min, date_max = df["Order Date"].min(), df["Order Date"].max()
date_range_sel = st.sidebar.date_input("Order Date Range", [date_min, date_max], min_value=date_min, max_value=date_max)

region_sel = st.sidebar.multiselect("Region", options=sorted(df["Region"].unique()), default=sorted(df["Region"].unique()))
category_sel = st.sidebar.multiselect("Category", options=sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))
segment_sel = st.sidebar.multiselect("Segment", options=sorted(df["Segment"].unique()), default=sorted(df["Segment"].unique()))

if len(date_range_sel) == 2:
    start_date, end_date = pd.Timestamp(date_range_sel[0]), pd.Timestamp(date_range_sel[1])
else:
    start_date, end_date = date_min, date_max

filtered = df[
    (df["Order Date"] >= start_date) & (df["Order Date"] <= end_date) &
    (df["Region"].isin(region_sel)) &
    (df["Category"].isin(category_sel)) &
    (df["Segment"].isin(segment_sel))
]

st.sidebar.markdown("---")
st.sidebar.download_button(
    "⬇️ Download Filtered Data (CSV)",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="superstore_filtered.csv",
    mime="text/csv",
)

# ---------------------------------------------------------------------------
# Header + KPIs
# ---------------------------------------------------------------------------

st.title("📊 Superstore Sales Dashboard")
st.caption("Interactive sales, product, shipping, and regional analysis")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${filtered['Sales'].sum():,.0f}")
col2.metric("Total Profit", f"${filtered['Profit'].sum():,.0f}")
col3.metric("Orders", f"{len(filtered):,}")
col4.metric("Avg. Discount", f"{filtered['Discount'].mean():.0%}" if len(filtered) else "—")

st.divider()

# ---------------------------------------------------------------------------
# Sales Trend
# ---------------------------------------------------------------------------

st.subheader("Sales Trend Over Time")
trend = filtered.set_index("Order Date").resample("ME")["Sales"].sum().reset_index()
fig_trend = px.line(trend, x="Order Date", y="Sales", markers=True)
fig_trend.update_layout(height=350, margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig_trend, use_container_width=True)

# ---------------------------------------------------------------------------
# Product performance
# ---------------------------------------------------------------------------

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Sales by Category")
    cat_sales = filtered.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig_cat = px.bar(cat_sales, x="Category", y="Sales", color="Category")
    fig_cat.update_layout(height=350, showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_cat, use_container_width=True)

with col_b:
    st.subheader("Top Sub-Categories by Profit")
    subcat_profit = filtered.groupby("Sub-Category", as_index=False)["Profit"].sum().sort_values("Profit", ascending=False).head(8)
    fig_subcat = px.bar(subcat_profit, x="Profit", y="Sub-Category", orientation="h", color="Profit", color_continuous_scale="RdYlGn")
    fig_subcat.update_layout(height=350, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_subcat, use_container_width=True)

# ---------------------------------------------------------------------------
# Shipping analysis
# ---------------------------------------------------------------------------

col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Orders by Ship Mode")
    ship_counts = filtered["Ship Mode"].value_counts().reset_index()
    ship_counts.columns = ["Ship Mode", "Orders"]
    fig_ship = px.pie(ship_counts, names="Ship Mode", values="Orders", hole=0.4)
    fig_ship.update_layout(height=350, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_ship, use_container_width=True)

with col_d:
    st.subheader("Sales by Region")
    region_sales = filtered.groupby("Region", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig_region = px.bar(region_sales, x="Region", y="Sales", color="Region")
    fig_region.update_layout(height=350, showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_region, use_container_width=True)

# ---------------------------------------------------------------------------
# Raw data view
# ---------------------------------------------------------------------------

with st.expander("View Filtered Raw Data"):
    st.dataframe(filtered, use_container_width=True)
