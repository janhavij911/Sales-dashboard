# Superstore Sales Dashboard

An interactive sales analytics dashboard built two ways — as a Python/Streamlit web app and as a Power BI report — using the same underlying dataset.

## Why Two Platforms

This project was originally inspired by a reference repository whose source code wasn't publicly available, so the dashboard was rebuilt from scratch. It was then extended further by building the identical analysis a second way in Power BI, to demonstrate both code-first analytics and low-code BI tooling on one consistent data model.

## The Dataset

2,000 synthetic but realistic orders, generated in code (`superstore_data.csv`):
- **Weighted categories**: Office Supplies (45%), Technology (30%), Furniture (25%) — not flat random
- **Gamma-distributed sales values** — right-skewed, like real order data: many small orders, fewer large ones
- **Randomized profit margin** (-15% to +35% per order) — some orders realistically show a loss
- **Fixed random seed** — reproducible, so both dashboards show identical numbers

Fields: Order ID, Order Date, Category, Sub-Category, Region, State, Segment, Ship Mode, Sales, Profit, Quantity, Discount.

## Architecture
superstore_data.csv
│
├──────────────► Streamlit App (Python + Plotly)
│ Code-first, interactive, deployable as a web app
│
└──────────────► Power BI Report
Drag-and-drop visuals, business-stakeholder-friendly


## The Streamlit App

- **Sidebar filters**: date range, Region, Category, Segment
- **KPI cards**: Total Sales, Total Profit, Orders, Avg. Discount — update live with filters
- **Charts**: monthly sales trend (line), sales by category (bar), top sub-categories by profit (horizontal bar), orders by ship mode (donut), sales by region (bar)
- **Export**: download the filtered data slice as CSV
- `@st.cache_data` keeps the dataset in memory so every filter interaction is instant

## The Power BI Dashboard

Same dataset, same metrics, built with native Power BI visuals:

| Streamlit | Power BI |
|---|---|
| `st.metric()` cards | Card visuals |
| `px.line()` trend chart | Line Chart visual |
| `px.bar()` category/region | Clustered Column/Bar |
| `px.pie()` ship mode | Donut Chart |
| `st.sidebar` filters | Slicers (cross-filter natively) |

Power BI's visuals cross-filter each other automatically — clicking a bar filters every other chart on the page without any extra code.

## Running the Streamlit App

```bash
pip install streamlit pandas numpy plotly
streamlit run superstore_dashboard.py
```

## Opening the Power BI Dashboard

Open `superstore_dashboard.pbix` in Power BI Desktop, or import `superstore_data.csv` fresh via Get Data → Text/CSV and rebuild using the visual mapping above.

## Tech Stack

Python, Streamlit, Plotly, Pandas, NumPy, Power BI Desktop

## Why Build It Both Ways

- **Streamlit**: version-controllable in Git, deployable as a live web app, fully custom logic — best for developer-facing tools
- **Power BI**: native to the Microsoft ecosystem, familiar to business stakeholders, no-code and fast to build — best for enterprise reporting

Being able to build the same analysis either way — as a developer tool or a business-facing BI report — demonstrates range across both ends of the analytics stack.

## Demo

![Streamlit Dashboard](streamlit_screenshot.png)
![Power BI Dashboard](powerbi_screenshot.png)

## Part of a Connected Portfolio

One of five connected projects demonstrating Azure AI document processing, Databricks data pipelines, autonomous AI agents, and a from-scratch RAG system alongside this dual-platform analytics dashboard.
