"""Streamlit dashboard for the telecom retention case study."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path
from streamlit.components.v1 import html as st_html

ROOT = Path(__file__).resolve().parent
# Handle both local and deployed paths
if (ROOT / "data_science_project").exists():
    # We're in the deployed environment
    ROOT = ROOT / "data_science_project"

DATA_PATH = ROOT / "data" / "processed" / "clean_dataset.csv"
SEGMENTED_PATH = ROOT / "data" / "processed" / "segmented.csv"
SEGMENT_SUMMARY_PATH = ROOT / "reports" / "segment_summary.csv"
REPO_URL = "https://github.com/Theoldmanname/data_science_project01_churn"
REPO_SUBDIR = "data_science_project"
REPO_BRANCH = "master"

# Provide more helpful error messages
if not DATA_PATH.exists():
    raise FileNotFoundError(f"Required data file not found at {DATA_PATH}. Please ensure the processed data files are generated.")


@st.cache_data(show_spinner=False)
def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    clean = pd.read_csv(DATA_PATH, parse_dates=["signup_date", "last_seen"])
    segmented = pd.read_csv(SEGMENTED_PATH, parse_dates=["signup_date", "last_seen"])
    segment_summary = pd.read_csv(SEGMENT_SUMMARY_PATH)
    return clean, segmented, segment_summary


def layout_header(clean: pd.DataFrame) -> None:
    st.title("Telecom Retention & Growth Dashboard")
    st.caption(
        "Executive dashboard extracted from the full data science case study. "
        "Use the controls to explore churn, spend, and segment insights."
    )

    churn_rate = clean["churned"].mean() * 100
    app_adoption = clean["has_app"].mean() * 100
    high_support = (clean["support_tickets_per_month"] >= 0.5).mean() * 100
    next_month_spend = clean["next_month_spend"].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Customers Analysed", f"{len(clean):,}")
    col2.metric("Churn Rate", f"{churn_rate:.1f}%")
    col3.metric("App Adoption", f"{app_adoption:.1f}%")
    col4.metric("Avg Next-Month Spend", f"$ {next_month_spend:.2f}")


def section_kpi_table(clean: pd.DataFrame) -> None:
    st.subheader("Portfolio Snapshot")
    metrics = {
        "Total Customers": f"{len(clean):,}",
        "Churn Rate": f"{clean['churned'].mean() * 100:.1f}%",
        "App Adoption": f"{clean['has_app'].mean() * 100:.1f}%",
        "High Support Load (>=0.5 tickets/mo)": f"{(clean['support_tickets_per_month'] >= 0.5).mean() * 100:.1f}%",
        "Average Monthly Revenue": f"$ {clean['avg_monthly_revenue'].mean():.2f}",
        "Next-Month Spend Forecast": f"$ {clean['next_month_spend'].mean():.2f}",
    }
    table_df = pd.DataFrame(list(metrics.items()), columns=["KPI", "Value"])
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(values=["KPI", "Value"], fill_color="#0d6efd", font=dict(color="white"), align="left"),
                cells=dict(values=[table_df["KPI"], table_df["Value"]], fill_color="#f8f9fa", align="left"),
            )
        ]
    )
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=250)
    st.plotly_chart(fig, use_container_width=True)


def section_filters(clean: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filters")
    plan = st.sidebar.multiselect(
        "Plan Type", options=sorted(clean["plan_type"].unique()), default=None
    )
    province = st.sidebar.multiselect(
        "Province", options=sorted(clean["province"].unique()), default=None
    )
    support_band = st.sidebar.selectbox(
        "Support Intensity",
        options=[
            "All",
            "Low (<=0.2 tickets/mo)",
            "Moderate (0.2-0.5 tickets/mo)",
            "High (>=0.5 tickets/mo)",
        ],
    )

    filtered = clean.copy()
    if plan:
        filtered = filtered[filtered["plan_type"].isin(plan)]
    if province:
        filtered = filtered[filtered["province"].isin(province)]
    if support_band != "All":
        if support_band.startswith("Low"):
            filtered = filtered[filtered["support_tickets_per_month"] <= 0.2]
        elif support_band.startswith("Moderate"):
            filtered = filtered[
                (filtered["support_tickets_per_month"] > 0.2)
                & (filtered["support_tickets_per_month"] < 0.5)
            ]
        else:
            filtered = filtered[filtered["support_tickets_per_month"] >= 0.5]
    return filtered


def section_trends(filtered: pd.DataFrame, title_suffix: str) -> None:
    st.subheader("Churn & Spend Trends")
    metrics = (
        filtered.assign(month=filtered["last_seen"].dt.to_period("M"))
        .groupby("month")
        .agg(churn_rate=("churned", "mean"), next_spend=("next_month_spend", "mean"))
        .reset_index()
    )
    metrics["month"] = metrics["month"].dt.to_timestamp()

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=metrics["month"],
            y=metrics["churn_rate"] * 100,
            name="Churn rate (%)",
            marker_color="#d63384",
            opacity=0.6,
            yaxis="y",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=metrics["month"],
            y=metrics["next_spend"],
            name="Next month spend (USD)",
            line=dict(color="#0d6efd", width=3),
            yaxis="y2",
        )
    )
    fig.update_layout(
        title=f"Churn & Spend Trend {title_suffix}",
        xaxis_title="Month",
        yaxis=dict(title="Churn rate (%)", rangemode="tozero"),
        yaxis2=dict(
            title="Next month spend (USD)", overlaying="y", side="right", rangemode="tozero"
        ),
        legend=dict(orientation="h", y=1.15, x=0.05),
        margin=dict(l=30, r=30, t=60, b=30),
    )
    st.plotly_chart(fig, use_container_width=True)


def section_plan_app(filtered: pd.DataFrame) -> None:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Churn by Plan Tier**")
        plan_churn = (
            filtered.groupby("plan_type")["churned"].mean().sort_values(ascending=False)
        )
        fig = px.bar(
            plan_churn * 100,
            labels={"value": "Churn Rate (%)", "index": "Plan Type"},
            color=plan_churn.index,
        )
        fig.update_layout(showlegend=False, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Churn by App Adoption**")
        app_churn = filtered.groupby("has_app")["churned"].mean().rename(
            {True: "Has App", False: "No App"}
        )
        fig = px.bar(
            app_churn * 100,
            labels={"value": "Churn Rate (%)", "index": "Segment"},
            color=app_churn.index,
        )
        fig.update_layout(showlegend=False, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)


def section_support_churn(filtered: pd.DataFrame) -> None:
    st.subheader("Support Load vs Churn")
    if filtered.empty:
        st.info("No data available for the current filter selection.")
        return

    max_support = filtered["support_tickets_per_month"].max()
    if pd.isna(max_support):
        st.info("Support information unavailable for the selected filters.")
        return

    upper_bound = max(1.51, float(max_support) + 0.01)
    support_bins = pd.cut(
        filtered["support_tickets_per_month"],
        bins=[-0.01, 0.2, 0.5, 1.5, upper_bound],
        labels=["0-0.2", "0.2-0.5", "0.5-1.5", ">1.5"],
    )
    support_churn = (
        filtered.assign(support_segment=support_bins)
        .groupby("support_segment")["churned"]
        .mean()
        .mul(100)
        .reindex(["0-0.2", "0.2-0.5", "0.5-1.5", ">1.5"])
        .dropna()
    )
    if support_churn.empty:
        st.info("No support ticket data available for charting.")
        return

    fig = px.bar(
        support_churn,
        labels={"index": "Support tickets per month", "value": "Churn rate (%)"},
        text_auto=".1f",
        color=support_churn.values,
        color_continuous_scale="magma",
    )
    fig.update_layout(showlegend=False, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)


def section_segments(segmented: pd.DataFrame, summary: pd.DataFrame) -> None:
    st.subheader("Segmentation Personas")
    st.dataframe(
        summary.rename(
            columns={
                "monthly_charges_mean": "Monthly Charges",
                "data_usage_mean": "Data Usage (GB)",
                "support_mean": "Support Tickets/mo",
                "churn_prob_mean": "Churn Probability",
                "next_month_spend_mean": "Next Month Spend",
                "app_penetration_pct": "App Penetration (%)",
            }
        ),
        use_container_width=True,
    )

    st.markdown("**Explore Cluster Composition**")
    cluster = st.selectbox(
        "Choose cluster", options=sorted(segmented["cluster"].unique()), index=0
    )
    cluster_slice = segmented[segmented["cluster"] == cluster]
    col1, col2, col3 = st.columns(3)
    col1.metric("Customers", f"{len(cluster_slice):,}")
    col2.metric(
        "Churn Probability",
        f"{cluster_slice['churn_probability'].mean():.2f}",
    )
    col3.metric(
        "Avg Support Tickets",
        f"{cluster_slice['support_tickets_per_month'].mean():.2f}",
    )

    fig = px.scatter(
        cluster_slice,
        x="pc1",
        y="pc2",
        color="retention_segment",
        hover_data=["customer_id", "monthly_charges", "next_month_spend"],
        labels={"pc1": "PC 1", "pc2": "PC 2", "retention_segment": "Retention Segment"},
    )
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)


def section_geo_churn(filtered: pd.DataFrame) -> None:
    st.subheader("Provincial Churn Hotspots")
    if filtered.empty:
        st.info("No data available for the current filter selection.")
        return

    province_summary = (
        filtered.groupby("province")
        .agg(
            customers=("customer_id", "count"),
            churn_rate=("churned", "mean"),
            lat=("lat", "mean"),
            lng=("lng", "mean"),
        )
        .dropna(subset=["lat", "lng"])
        .reset_index()
    )
    if province_summary.empty:
        st.info("Geographic information unavailable for the selected filters.")
        return

    fig = px.scatter_geo(
        province_summary,
        lat="lat",
        lon="lng",
        size="customers",
        size_max=30,
        color="churn_rate_pct",
        hover_name="province",
        hover_data={
            "customers": True,
            "churn_rate_pct": True,
        },
        color_continuous_scale="Viridis",
        projection="natural earth",
    )
    fig.update_layout(
        title="Customer footprint — bubble size reflects customer count, color reflects churn rate",
        margin=dict(l=0, r=0, t=50, b=0),
    )
    st.plotly_chart(fig, use_container_width=True)


def section_resources() -> None:
    st.subheader("Reports & Downloads")
    pages_base = "https://Theoldmanname.github.io/data_science_project01_churn"

    st.markdown(
        f"""
        - [Insight Summary PDF]({pages_base}/insight_summary.pdf)
        - [EDA Profiling Report (download)]({pages_base}/eda_report.html) | [View online]({pages_base}/eda_report.html)
        - [Segment Summary CSV]({pages_base}/segment_summary.csv)
        - [Segmented Dataset]({pages_base}/segmented.csv)
        - [GitHub Repository]({REPO_URL})
        """
    )

    with st.expander("Preview EDA report inline"):
        try:
            eda_html = (ROOT / "reports" / "eda_report.html").read_text(
                encoding="utf-8"
            )
            st_html(eda_html, height=600, scrolling=True)
        except FileNotFoundError:
            st.info("EDA report not found locally. Ensure `reports/eda_report.html` exists.")


def main() -> None:
    clean, segmented, summary = load_data()
    layout_header(clean)
    section_kpi_table(clean)
    filtered = section_filters(clean)

    title_suffix = ""
    if len(filtered) != len(clean):
        title_suffix = f"(Filtered sample: {len(filtered):,} customers)"
    section_trends(filtered, title_suffix)
    section_plan_app(filtered)
    section_support_churn(filtered)
    section_geo_churn(filtered)
    section_segments(segmented, summary)
    section_resources()

    st.markdown("---")
    st.markdown(
        "Built with ❤️ using Streamlit. Source notebooks and full case study: "
        "[GitHub Repository](https://github.com/Theoldmanname/data_science_project01_churn)."
    )


if __name__ == "__main__":
    main()
