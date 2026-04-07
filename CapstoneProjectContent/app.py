import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Flight Delay Risk Dashboard", layout="wide")

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "artifact_scored_flights.parquet"

@st.cache_data
def load_data():
    df = pd.read_parquet(DATA_PATH)
    df["FLIGHT_DATE"] = pd.to_datetime(df["FLIGHT_DATE"], errors="coerce")
    return df

df = load_data()

st.sidebar.title("Filters")

date_min = df["FLIGHT_DATE"].min().date()
date_max = df["FLIGHT_DATE"].max().date()

date_range = st.sidebar.date_input(
    "Date range",
    value=(date_min, date_max),
    min_value=date_min,
    max_value=date_max
)

origin_options = ["All"] + sorted(df["ORIGIN"].dropna().astype(str).unique().tolist())
dest_options = ["All"] + sorted(df["DEST"].dropna().astype(str).unique().tolist())
route_options = ["All"] + sorted(df["ROUTE"].dropna().astype(str).unique().tolist())

origin_filter = st.sidebar.selectbox("Origin", origin_options)
dest_filter = st.sidebar.selectbox("Destination", dest_options)
route_filter = st.sidebar.selectbox("Route", route_options)

page = st.sidebar.radio("View", ["Summary", "Flight Search"])

filtered = df.copy()

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered = filtered[(filtered["FLIGHT_DATE"] >= start_date) & (filtered["FLIGHT_DATE"] <= end_date)]

if origin_filter != "All":
    filtered = filtered[filtered["ORIGIN"].astype(str) == origin_filter]

if dest_filter != "All":
    filtered = filtered[filtered["DEST"].astype(str) == dest_filter]

if route_filter != "All":
    filtered = filtered[filtered["ROUTE"].astype(str) == route_filter]

if page == "Summary":
    st.title("Flight Delay Risk Dashboard")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Flights", f"{len(filtered):,}")
    c2.metric("Avg Predicted Risk", f"{filtered['pred_prob'].mean():.2%}" if len(filtered) else "N/A")
    c3.metric("Observed Delay Rate", f"{filtered['actual_delay'].mean():.2%}" if len(filtered) else "N/A")
    c4.metric("Predicted Positive Rate", f"{filtered['pred_label'].mean():.2%}" if len(filtered) else "N/A")

    st.subheader("Predicted Risk Distribution")
    fig_hist = px.histogram(filtered, x="pred_prob", nbins=30, title="Predicted Delay Risk Distribution")
    st.plotly_chart(fig_hist, use_container_width=True)

    st.subheader("Daily Risk Trend")
    daily = (
        filtered.groupby("FLIGHT_DATE", as_index=False)
        .agg(
            flights=("pred_prob", "size"),
            observed_delay_rate=("actual_delay", "mean"),
            avg_predicted_risk=("pred_prob", "mean")
        )
    )
    fig_daily = px.line(
        daily,
        x="FLIGHT_DATE",
        y=["observed_delay_rate", "avg_predicted_risk"],
        title="Observed vs Predicted Delay Risk Over Time"
    )
    st.plotly_chart(fig_daily, use_container_width=True)

    st.subheader("Airport-Level Summary")
    airport_summary = (
        filtered.groupby("ORIGIN", as_index=False)
        .agg(
            flights=("ORIGIN", "size"),
            avg_predicted_risk=("pred_prob", "mean"),
            observed_delay_rate=("actual_delay", "mean")
        )
        .sort_values("avg_predicted_risk", ascending=False)
    )
    st.dataframe(airport_summary, use_container_width=True)

    st.subheader("Highest-Risk Routes")
    route_summary = (
        filtered.groupby("ROUTE", as_index=False)
        .agg(
            flights=("ROUTE", "size"),
            avg_predicted_risk=("pred_prob", "mean"),
            observed_delay_rate=("actual_delay", "mean")
        )
        .sort_values(["avg_predicted_risk", "flights"], ascending=[False, False])
        .head(20)
    )
    st.dataframe(route_summary, use_container_width=True)

else:
    st.title("Flight Search / Risk Explorer")

    show_cols = [
        "FLIGHT_DATE", "ORIGIN", "DEST", "ROUTE", "CARRIER_ROUTE",
        "pred_prob", "pred_label", "actual_delay",
        "route_observed_delay_rate", "origin_observed_delay_rate"
    ]
    show_cols = [c for c in show_cols if c in filtered.columns]

    st.subheader("Filtered Flights")
    st.dataframe(
        filtered[show_cols].sort_values(["FLIGHT_DATE", "pred_prob"], ascending=[True, False]),
        use_container_width=True
    )

    st.subheader("Grouped Risk View")
    group_choice = st.selectbox("Group by", ["ORIGIN", "DEST", "ROUTE"])

    grouped = (
        filtered.groupby(group_choice, as_index=False)
        .agg(
            flights=(group_choice, "size"),
            avg_predicted_risk=("pred_prob", "mean"),
            observed_delay_rate=("actual_delay", "mean")
        )
        .sort_values("avg_predicted_risk", ascending=False)
    )
    st.dataframe(grouped, use_container_width=True)
