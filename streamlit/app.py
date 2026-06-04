"""Olist Executive Dashboard — Streamlit.

Reads the dbt marts from the DuckDB warehouse (read-only) and presents
executive KPIs, growth, satisfaction drivers, category and geographic views.

Run:  streamlit run streamlit/app.py
"""
from pathlib import Path

import duckdb
import pandas as pd
import plotly.express as px
import streamlit as st

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "olist.duckdb"
NAVY, TEAL, ORANGE, GOLD = "#1f3b57", "#2a9d8f", "#e76f51", "#e9c46a"

st.set_page_config(page_title="Olist Executive Dashboard", page_icon="📦", layout="wide")


@st.cache_resource
def get_conn():
    if not DB_PATH.exists():
        st.error(f"Warehouse not found at {DB_PATH}. Run the pipeline first "
                 "(meltano run → dbt build).")
        st.stop()
    return duckdb.connect(str(DB_PATH), read_only=True)


@st.cache_data
def q(sql: str) -> pd.DataFrame:
    return get_conn().execute(sql).df()


st.title("📦 Olist — Executive Dashboard")
st.caption("Brazilian e-commerce · Sept 2016 – Oct 2018 · data via Meltano → dbt → DuckDB/Snowflake")

# ---- Sidebar filters ----
states = q("SELECT DISTINCT customer_state FROM analytics.fct_orders "
           "WHERE customer_state IS NOT NULL ORDER BY 1")["customer_state"].tolist()
sel_states = st.sidebar.multiselect("Filter by customer state", states, default=[])
state_clause = ""
if sel_states:
    joined = "','".join(sel_states)
    state_clause = f"WHERE customer_state IN ('{joined}')"

# ---- KPI row ----
kpi = q(f"""
SELECT count(*) orders, sum(gmv) gmv, sum(gmv)/count(distinct order_id) aov,
       avg(review_score) review,
       100.0*sum(CASE WHEN is_late THEN 1 ELSE 0 END)/
             nullif(sum(CASE WHEN delivered_at IS NOT NULL THEN 1 ELSE 0 END),0) late_pct
FROM analytics.fct_orders {state_clause}""").iloc[0]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total GMV", f"R$ {kpi.gmv/1e6:,.1f}M")
c2.metric("Orders", f"{int(kpi.orders):,}")
c3.metric("Avg Order Value", f"R$ {kpi.aov:,.0f}")
c4.metric("Avg Review", f"{kpi.review:.2f} ★")
c5.metric("Late Deliveries", f"{kpi.late_pct:.1f}%")

st.divider()

# ---- Growth ----
left, right = st.columns([3, 2])
with left:
    st.subheader("Monthly GMV growth")
    m = q("""SELECT order_month, gmv FROM analytics.fct_monthly_revenue
             WHERE order_month BETWEEN '2017-01' AND '2018-08' ORDER BY 1""")
    fig = px.line(m, x="order_month", y="gmv", markers=True)
    fig.update_traces(line_color=NAVY)
    fig.update_layout(height=340, yaxis_title="GMV (R$)", xaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Delivery → satisfaction")
    d = q("""SELECT CASE WHEN is_late THEN 'Late' ELSE 'On-time' END status,
             avg(review_score) score FROM analytics.fct_orders
             WHERE delivered_at IS NOT NULL GROUP BY 1""")
    fig = px.bar(d, x="status", y="score", color="status",
                 color_discrete_map={"On-time": TEAL, "Late": ORANGE}, text_auto=".2f")
    fig.update_layout(height=340, showlegend=False, yaxis_range=[0, 5], yaxis_title="Avg review")
    st.plotly_chart(fig, use_container_width=True)
    st.info("Late orders score **1.7 points lower** — delivery reliability is the top "
            "controllable satisfaction lever.")

st.divider()

# ---- Categories + Geography ----
left, right = st.columns(2)
with left:
    st.subheader("Top categories by revenue")
    cat = q("""SELECT category, revenue, avg_review_score
              FROM analytics.fct_category_performance ORDER BY revenue DESC LIMIT 10""")
    fig = px.bar(cat.sort_values("revenue"), x="revenue", y="category", orientation="h",
                 color_discrete_sequence=[TEAL])
    fig.update_layout(height=400, xaxis_title="Revenue (R$)", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Revenue by state")
    g = q(f"""SELECT customer_state, sum(gmv) gmv FROM analytics.fct_orders
             {state_clause if state_clause else ''}
             {'AND' if state_clause else 'WHERE'} customer_state IS NOT NULL
             GROUP BY 1 ORDER BY 2 DESC LIMIT 10""")
    fig = px.bar(g, x="customer_state", y="gmv",
                 color=g.customer_state.eq("SP").map({True: NAVY, False: GOLD}),
                 color_discrete_map="identity")
    fig.update_layout(height=400, yaxis_title="GMV (R$)", xaxis_title="", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.info("**São Paulo ≈ 38% of GMV** — concentration risk and expansion opportunity.")

st.divider()
rep = q("SELECT 100.0*sum(CASE WHEN is_repeat THEN 1 ELSE 0 END)/count(*) pct "
        "FROM analytics.dim_customers").iloc[0].pct
st.subheader("Retention")
st.metric("Repeat customer rate", f"{rep:.1f}%",
          help="Customers with more than one order")
st.warning("Only ~3% of customers reorder. Retention is the largest untapped growth lever.")
