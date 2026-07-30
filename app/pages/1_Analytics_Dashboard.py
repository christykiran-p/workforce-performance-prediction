import streamlit as st
import duckdb
import plotly.express as px

from src.security.authorization import (
    require_login
)

from src.security.authorization import (
    require_role
)

require_role(
    [
        "Admin",
        "Leadership",
        "HR"
    ]
)

st.set_page_config(
    page_title="Workforce Analytics Dashboard",
    layout="wide"
)

st.title("Workforce Analytics Dashboard")

st.markdown(
    """
    ### Workforce Performance Prediction Platform
    Data Engineering • Analytics • Workforce Intelligence
    """
)


@st.cache_data
def load_data():

    conn = duckdb.connect(
        "data/warehouse/workforce_analytics.duckdb",
        read_only=True
    )

    df = conn.execute("""
    SELECT *
    FROM employee_analytics
    """).fetchdf()

    conn.close()

    return df


df = load_data()

# ---------------------------------------------
# Analytics Population
# Exclude Department Owners (Employee IDs 1-7)
# ---------------------------------------------

analytics_population = df[
    df["avg_performance_score"].notna()
].copy()

# ---------------------------------------------
# Filters
# ---------------------------------------------

st.sidebar.header("Analytics Filters")

# Department Filter

departments = sorted(
    analytics_population["department"]
    .dropna()
    .unique()
    .tolist()
)

selected_departments = st.sidebar.multiselect(
    "Department(s)",
    options=departments,
    default=departments
)

if selected_departments:

    analytics_population = analytics_population[
        analytics_population["department"]
        .isin(selected_departments)
    ]

# Business Unit Filter

business_units = sorted(
    analytics_population["business_unit"]
    .dropna()
    .unique()
    .tolist()
)

selected_business_units = st.sidebar.multiselect(
    "Business Unit(s)",
    options=business_units,
    default=business_units
)

if selected_business_units:

    analytics_population = analytics_population[
        analytics_population["business_unit"]
        .isin(selected_business_units)
    ]

# Band Level Filter

band_levels = sorted(
    analytics_population["band_level"]
    .dropna()
    .unique()
    .tolist()
)

selected_band_levels = st.sidebar.multiselect(
    "Band Level(s)",
    options=band_levels,
    default=band_levels
)

if selected_band_levels:

    analytics_population = analytics_population[
        analytics_population["band_level"]
        .isin(selected_band_levels)
    ]

# Gender Filter

genders = sorted(
    analytics_population["gender"]
    .dropna()
    .unique()
    .tolist()
)

selected_genders = st.sidebar.multiselect(
    "Gender(s)",
    options=genders,
    default=genders
)

if selected_genders:

    analytics_population = analytics_population[
        analytics_population["gender"]
        .isin(selected_genders)
    ]

# Employment Type Filter

employment_types = sorted(
    analytics_population["employment_type"]
    .dropna()
    .unique()
    .tolist()
)

selected_employment_types = st.sidebar.multiselect(
    "Employment Type(s)",
    options=employment_types,
    default=employment_types
)

if selected_employment_types:

    analytics_population = analytics_population[
        analytics_population["employment_type"]
        .isin(selected_employment_types)
    ]

# ---------------------------------------------
# KPI Cards
# ---------------------------------------------

st.subheader("Workforce Analytics Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Analytics Population",
    len(analytics_population)
)

col2.metric(
    "Departments",
    analytics_population["department"].nunique()
)

col3.metric(
    "Avg Performance Score",
    round(
        analytics_population[
            "avg_performance_score"
        ].mean(),
        2
    )
)

col4.metric(
    "Attendance Rate (%)",
    round(
        analytics_population[
            "attendance_rate"
        ].mean(),
        2
    )
)

st.divider()

# ---------------------------------------------
# Executive Insights
# ---------------------------------------------

st.subheader("Executive Insights")

highest_performance_dept = (
    analytics_population
    .groupby("department")["avg_performance_score"]
    .mean()
    .idxmax()
)

highest_attendance_dept = (
    analytics_population
    .groupby("department")["attendance_rate"]
    .mean()
    .idxmax()
)

highest_salary_cost_dept = (
    analytics_population
    .groupby("department")["annual_salary"]
    .sum()
    .idxmax()
)

col1, col2, col3 = st.columns(3)

col1.success(
    f"🏆 Highest Performing Department\n\n{highest_performance_dept}"
)

col2.info(
    f"📈 Highest Attendance Department\n\n{highest_attendance_dept}"
)

col3.warning(
    f"💰 Highest Salary Cost Department\n\n{highest_salary_cost_dept}"
)

st.divider()

# ---------------------------------------------
# Performance Analytics
# ---------------------------------------------

st.subheader(
    "Average Performance by Department"
)

performance_df = (
    analytics_population
    .groupby("department")[
        "avg_performance_score"
    ]
    .mean()
    .reset_index()
    .sort_values(
        "avg_performance_score",
        ascending=True
    )
)

fig1 = px.bar(
    performance_df,
    x="avg_performance_score",
    y="department",
    orientation="h",
    title="Average Performance Score by Department",
    text="avg_performance_score"
)

fig1.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

# ---------------------------------------------
# Performance Threshold Lines
# ---------------------------------------------

# Below Average

fig1.add_vline(
    x=2.5,
    line_dash="dash",
    line_color="red"
)

# Average

fig1.add_vline(
    x=3.0,
    line_dash="dash",
    line_color="orange"
)

# Good

fig1.add_vline(
    x=3.5,
    line_dash="dash",
    line_color="gold"
)

# Very Good

fig1.add_vline(
    x=4.0,
    line_dash="dash",
    line_color="green"
)

# Excellent

fig1.add_vline(
    x=4.5,
    line_dash="dash",
    line_color="blue"
)

fig1.update_layout(
    xaxis_title="Average Performance Score",
    yaxis_title="Department",
    showlegend=False
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ---------------------------------------------
# Performance Threshold Legend
# ---------------------------------------------

st.caption(
    "Performance Threshold Meaning | "
    "🔴 <2.5 Below Average | "
    "🟠 3.0 Average | "
    "🟡 3.5 Good | "
    "🟢 4.0 Very Good | "
    "🔵 4.5+ Excellent"
)

# ---------------------------------------------
# Attendance Analytics
# ---------------------------------------------

st.subheader(
    "Average Attendance by Department"
)

attendance_df = (
    analytics_population
    .groupby("department")[
        "attendance_rate"
    ]
    .mean()
    .reset_index()
    .sort_values(
        "attendance_rate",
        ascending=True
    )
)

fig2 = px.bar(
    attendance_df,
    x="attendance_rate",
    y="department",
    orientation="h",
    title="Attendance Rate by Department",
    text="attendance_rate"
)

fig2.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

# ---------------------------------------------
# Threshold Lines
# ---------------------------------------------

fig2.add_vline(
    x=80,
    line_dash="dash",
    line_color="orange"
)

fig2.add_vline(
    x=85,
    line_dash="dash",
    line_color="green"
)

fig2.add_vline(
    x=90,
    line_dash="dash",
    line_color="blue"
)

fig2.update_layout(
    xaxis_title="Attendance Rate (%)",
    yaxis_title="Department",
    showlegend=False
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ---------------------------------------------
# Threshold Legend
# ---------------------------------------------

st.caption(
    "Threshold Line Meaning | "
    "🟠 80% Minimum Acceptable Attendance | "
    "🟢 85% Target Attendance | "
    "🔵 90% Excellence Benchmark"
)

# ---------------------------------------------
# Leave Analytics
# ---------------------------------------------

st.subheader(
    "Average Leave Usage by Department"
)

leave_df = (
    analytics_population
    .groupby("department")[
        "total_leave_used"
    ]
    .mean()
    .reset_index()
    .sort_values(
        "total_leave_used",
        ascending=True
    )
)

fig3 = px.bar(
    leave_df,
    x="total_leave_used",
    y="department",
    orientation="h",
    title="Leave Usage by Department",
    text="total_leave_used"
)

fig3.update_traces(
    texttemplate="%{text:.1f}",
    textposition="outside"
)

# ---------------------------------------------
# Dynamic Leave Thresholds
# ---------------------------------------------

TOTAL_ANNUAL_LEAVE = 27
MONTHS_OF_DATA = 7

max_expected_leave = (
    TOTAL_ANNUAL_LEAVE / 12
) * MONTHS_OF_DATA

threshold_50 = round(
    max_expected_leave * 0.50,
    2
)

threshold_75 = round(
    max_expected_leave * 0.75,
    2
)

threshold_100 = round(
    max_expected_leave,
    2
)

# 50% Utilization

fig3.add_vline(
    x=threshold_50,
    line_dash="dash",
    line_color="orange"
)

# 75% Utilization

fig3.add_vline(
    x=threshold_75,
    line_dash="dash",
    line_color="green"
)

# 100% Utilization

fig3.add_vline(
    x=threshold_100,
    line_dash="dash",
    line_color="blue"
)

fig3.update_layout(
    xaxis_title="Average Leave Used (Days)",
    yaxis_title="Department",
    showlegend=False
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ---------------------------------------------
# Leave Threshold Legend
# ---------------------------------------------

st.caption(
    f"Leave Threshold Meaning | "
    f"🟠 50% Utilization = {threshold_50} days | "
    f"🟢 75% Utilization = {threshold_75} days | "
    f"🔵 100% Utilization = {threshold_100} days "
    f"(Based on 27 annual leave entitlement prorated for {MONTHS_OF_DATA} months)")

# ---------------------------------------------
# Salary Distribution
# ---------------------------------------------

st.subheader("Salary Distribution")

salary_df = (
    analytics_population
    .groupby("department")["annual_salary"]
    .mean()
    .reset_index()
    .sort_values(
        "annual_salary",
        ascending=True
    )
)

fig4 = px.bar(
    salary_df,
    x="annual_salary",
    y="department",
    orientation="h",
    title="Average Salary by Department",
    text="annual_salary"
)

fig4.update_traces(
    texttemplate="₹%{text:,.0f}",
    textposition="outside"
)

fig4.update_layout(
    xaxis_title="Average Annual Salary",
    yaxis_title="Department"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ---------------------------------------------
# Workforce Distribution
# ---------------------------------------------

st.subheader(
    "Workforce Distribution by Department"
)

workforce_df = (
    analytics_population
    .groupby("department")
    .size()
    .reset_index(name="employee_count")
    .sort_values(
        "employee_count",
        ascending=True
    )
)

fig5 = px.bar(
    workforce_df,
    x="employee_count",
    y="department",
    orientation="h",
    title="Employee Count by Department"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# ---------------------------------------------
# Salary Cost Contribution
# ---------------------------------------------

st.subheader(
    "Salary Cost Contribution by Department"
)

salary_cost_df = (
    analytics_population
    .groupby("department")["annual_salary"]
    .sum()
    .reset_index()
)

total_salary_cost = (
    salary_cost_df["annual_salary"]
    .sum()
)

salary_cost_df["salary_contribution_pct"] = (
    salary_cost_df["annual_salary"]
    / total_salary_cost
    * 100
)

salary_cost_df = salary_cost_df.sort_values(
    "salary_contribution_pct",
    ascending=True
)

fig6 = px.bar(
    salary_cost_df,
    x="salary_contribution_pct",
    y="department",
    orientation="h",
    title="Salary Cost Contribution by Department",
    text="salary_contribution_pct"
)

fig6.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig6.update_layout(
    xaxis_title="Salary Cost Contribution (%)",
    yaxis_title="Department"
)

st.plotly_chart(
    fig6,
    use_container_width=True
)

# ---------------------------------------------
# Data Quality Summary
# ---------------------------------------------

st.subheader("Data Quality Summary")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Employees",
    len(df)
)

col2.metric(
    "Analytics Population",
    len(analytics_population)
)

col3.metric(
    "Leadership Exemptions",
    len(df) - len(analytics_population)
)

# ---------------------------------------------
# Export Analytics Dataset
# ---------------------------------------------

st.subheader("Export Analytics Data")

csv = analytics_population.to_csv(index=False)

st.download_button(
    label="📥 Download Analytics Dataset (CSV)",
    data=csv,
    file_name="analytics_dataset.csv",
    mime="text/csv"
)

# ---------------------------------------------
# Dataset Preview
# ---------------------------------------------

st.subheader("Analytics Dataset Preview")

st.dataframe(
    analytics_population.head(50),
    use_container_width=True
)