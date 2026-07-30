import streamlit as st
import pandas as pd
import plotly.express as px

from src.security.data_access import (
    get_accessible_employee_ids
)

from src.security.authorization import (
    require_role
)

require_role(
    [
        "Admin",
        "Leadership",
        "HR",
        "Manager"
    ]
)

accessible_employee_ids = (
    get_accessible_employee_ids(
        st.session_state.employee_id,
        st.session_state.role
    )
)

st.set_page_config(
    page_title="Prediction Dashboard",
    layout="wide"
)

st.title("Prediction Intelligence Dashboard")

# =====================================================
# Load Data
# =====================================================

@st.cache_data
def load_prediction_data():

    prediction_df = pd.read_csv(
        "reports/prediction_output.csv"
    )

    model_df = pd.read_csv(
        "reports/model_comparison.csv"
    )

    feature_df = pd.read_csv(
        "reports/feature_importance.csv"
    )

    return prediction_df, model_df, feature_df


prediction_df, model_df, feature_df = (
    load_prediction_data()
)

prediction_df = prediction_df[
    prediction_df["employee_id"].isin(
        accessible_employee_ids
    )
]

# =====================================================
# Remove Missing Predictions
# =====================================================

prediction_df = prediction_df[
    prediction_df[
        "predicted_performance_score"
    ].notna()
]

# =====================================================
# Sidebar Filters
# =====================================================

st.sidebar.header(
    "Prediction Filters"
)

selected_departments = (
    st.sidebar.multiselect(
        "Department",
        sorted(
            prediction_df["department"]
            .dropna()
            .unique()
            .tolist()
        ),
        default=sorted(
            prediction_df["department"]
            .dropna()
            .unique()
            .tolist()
        )
    )
)

prediction_df = prediction_df[
    prediction_df["department"]
    .isin(selected_departments)
]

# =====================================================
# Model Performance Summary - 1
# =====================================================

st.subheader(
    "Model Performance Summary - 1"
)

elasticnet_metrics = model_df[
    model_df["model_name"]
    .str.contains(
        "Elastic",
        case=False,
        na=False
    )
]

if len(elasticnet_metrics) > 0:

    metrics = elasticnet_metrics.iloc[0]

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Best Model",
        metrics["model_name"]
    )

    col2.metric(
        "CV RMSE",
        round(
            metrics["cv_rmse"],
            3
        )
    )

    col3.metric(
        "Test RMSE",
        round(
            metrics["test_rmse"],
            3
        )
    )

    col4.metric(
        "Test MAE",
        round(
            metrics["test_mae"],
            3
        )
    )

    col5.metric(
        "Test R²",
        round(
            metrics["test_r2"],
            3
        )
    )

st.divider()

# =====================================================
# Model Performance Summary - 2
# =====================================================

st.markdown(
    """
    <style>
    div[data-testid="stMetricValue"] {
        font-size: 1.2rem;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.subheader(
    "Model Performance Summary - 2"
)



# =====================================================
# Prediction Overview KPIs
# =====================================================

st.subheader(
    "Prediction Overview"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Predictions Generated",
    len(prediction_df)
)

col2.metric(
    "Average Predicted Score",
    round(
        prediction_df[
            "predicted_performance_score"
        ].mean(),
        2
    )
)

col3.metric(
    "Highest Predicted Score",
    round(
        prediction_df[
            "predicted_performance_score"
        ].max(),
        2
    )
)

col4.metric(
    "Lowest Predicted Score",
    round(
        prediction_df[
            "predicted_performance_score"
        ].min(),
        2
    )
)

st.divider()

# =====================================================
# Dashboard Health Check
# =====================================================

st.subheader(
    "Prediction Coverage Summary"
)

total_employees = 495

predictions_generated = len(
    prediction_df
)

excluded_employees = (
    total_employees
    - predictions_generated
)

coverage = round(
    (
        predictions_generated
        / total_employees
    ) * 100,
    2
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Employees",
    total_employees
)

col2.metric(
    "Predictions Generated",
    predictions_generated
)

col3.metric(
    "Excluded Employees",
    excluded_employees
)

col4.metric(
    "Coverage %",
    coverage
)

st.divider()

# =====================================================
# Prediction Distribution (Bell Curve)
# =====================================================

st.subheader(
    "Predicted Performance Distribution"
)

mean_score = (
    prediction_df[
        "predicted_performance_score"
    ]
    .mean()
)

fig_bell = px.histogram(
    prediction_df,
    x="predicted_performance_score",
    nbins=20,
    title="Predicted Performance Distribution"
)

fig_bell.add_vline(
    x=mean_score,
    line_dash="dash",
    annotation_text="Mean Score"
)

st.plotly_chart(
    fig_bell,
    use_container_width=True
)

st.divider()

# =====================================================
# Executive Prediction Insights
# =====================================================

st.subheader(
    "Executive Prediction Insights"
)

highest_department = (
    prediction_df
    .groupby("department")[
        "predicted_performance_score"
    ]
    .mean()
    .idxmax()
)

highest_employee = (
    prediction_df
    .sort_values(
        "predicted_performance_score",
        ascending=False
    )
    .iloc[0]
)

at_risk_department = (
    prediction_df[
        prediction_df[
            "predicted_performance_score"
        ] < 3.0
    ]
    .groupby("department")
    .size()
    .idxmax()
)

top_feature = (
    feature_df
    .sort_values(
        "absolute_coefficient",
        ascending=False
    )
    .iloc[0]["feature"]
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🏆 Highest Predicted Department",
    highest_department
)

col2.metric(
    "⭐ Highest Predicted Employee",
    f"{highest_employee['first_name']} {highest_employee['last_name']}"
)

col3.metric(
    "⚠ Most At-Risk Department",
    at_risk_department
)

col4.metric(
    "🎯 Top Driver",
    top_feature
)

st.divider()


# =====================================================
# Prediction Category Distribution
# =====================================================

st.subheader(
    "Prediction Category Distribution"
)

category_df = (
    prediction_df[
        "prediction_category"
    ]
    .value_counts()
    .reset_index()
)

category_df.columns = [
    "prediction_category",
    "count"
]

fig1 = px.pie(
    category_df,
    names="prediction_category",
    values="count",
    hole=0.5,
    title="Prediction Category Distribution"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.divider()

# =====================================================
# STAR Distribution
# =====================================================

st.subheader(
    "STAR Workforce Distribution"
)

star_df = prediction_df.copy()

star_df["star_category"] = pd.cut(
    star_df["predicted_performance_score"],
    bins=[0, 3.0, 3.5, 4.0, 4.5, 5.0],
    labels=[
        "At Risk",
        "Average Performer",
        "Strong Contributor",
        "High Performer",
        "Superstar"
    ]
)

star_summary = (
    star_df["star_category"]
    .value_counts()
    .reset_index()
)

star_summary.columns = [
    "Category",
    "Employees"
]

fig_star = px.bar(
    star_summary,
    x="Category",
    y="Employees",
    title="STAR Workforce Segmentation"
)

st.plotly_chart(
    fig_star,
    use_container_width=True
)

st.divider()

# =====================================================
# Prediction Threshold Distribution
# =====================================================

st.subheader(
    "Prediction Threshold Distribution"
)

threshold_df = prediction_df.copy()

threshold_df["performance_band"] = pd.cut(
    threshold_df["predicted_performance_score"],
    bins=[0, 3.0, 3.5, 4.0, 4.5, 5.0],
    labels=[
        "At Risk",
        "Average",
        "Good",
        "Very Good",
        "Excellent"
    ]
)

band_summary = (
    threshold_df[
        "performance_band"
    ]
    .value_counts()
    .reset_index()
)

band_summary.columns = [
    "Performance Band",
    "Employees"
]

fig_band = px.bar(
    band_summary,
    x="Performance Band",
    y="Employees",
    title="Employees by Prediction Band"
)

st.plotly_chart(
    fig_band,
    use_container_width=True
)

st.divider()


# =====================================================
# Predicted Performance by Department
# =====================================================

st.subheader(
    "Predicted Performance by Department"
)

dept_prediction_df = (
    prediction_df
    .groupby("department")[
        "predicted_performance_score"
    ]
    .mean()
    .reset_index()
    .sort_values(
        "predicted_performance_score",
        ascending=True
    )
)

fig2 = px.bar(
    dept_prediction_df,
    x="predicted_performance_score",
    y="department",
    orientation="h",
    title="Average Predicted Performance by Department"
)

fig2.add_vline(
    x=2.5,
    line_dash="dash",
    annotation_text="Below Average"
)

fig2.add_vline(
    x=3.0,
    line_dash="dash",
    annotation_text="Average"
)

fig2.add_vline(
    x=3.5,
    line_dash="dash",
    annotation_text="Good"
)

fig2.add_vline(
    x=4.0,
    line_dash="dash",
    annotation_text="Very Good"
)

fig2.add_vline(
    x=4.5,
    line_dash="dash",
    annotation_text="Excellent"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.divider()

# =====================================================
# Department Prediction Comparison
# =====================================================

st.subheader(
    "Department Prediction Comparison"
)

dept_order = (
    prediction_df
    .groupby("department")[
        "predicted_performance_score"
    ]
    .mean()
    .sort_values(
        ascending=False
    )
    .index
)

fig_box = px.box(
    prediction_df,
    x="department",
    y="predicted_performance_score",
    category_orders={
        "department": dept_order.tolist()
    },
    title="Prediction Distribution by Department"
)

st.plotly_chart(
    fig_box,
    use_container_width=True
)

st.info(
    """
    Key Insights

    • Product has the highest median predicted performance.

    • Technology has the largest workforce but not the highest predicted performance.

    • Operations, Procurement and Governance show stable performance distributions.

    • Sales and Marketing exhibit greater performance variability.

    • Delivery contains high-performing outliers.
    """
)

st.divider()

# =====================================================
# Top Predicted Performers
# =====================================================

st.subheader(
    "Top Predicted Performers"
)

top_performers = (
    prediction_df
    .sort_values(
        "predicted_performance_score",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_performers[
        [
            "employee_id",
            "first_name",
            "last_name",
            "department",
            "job_title",
            "predicted_performance_score"
        ]
    ],
    use_container_width=True
)

st.divider()

# =====================================================
# At-Risk Employees
# =====================================================

st.subheader(
    "At-Risk Employees"
)

at_risk_df = prediction_df[
    prediction_df[
        "predicted_performance_score"
    ] < 3.0
]

st.dataframe(
    at_risk_df[
        [
            "employee_id",
            "first_name",
            "last_name",
            "department",
            "job_title",
            "predicted_performance_score"
        ]
    ],
    use_container_width=True
)

top_csv = top_performers.to_csv(
    index=False
)

st.download_button(
    "📥 Download Top Performers",
    top_csv,
    "top_performers.csv",
    "text/csv"
)


st.divider()


# =====================================================
# Feature Importance
# =====================================================

st.subheader(
    "Top Feature Importance Drivers"
)

feature_df["feature"] = (
    feature_df["feature"]
    .str.replace(
        "numeric__",
        "",
        regex=False
    )
    .str.replace(
        "_",
        " ",
        regex=False
    )
    .str.title()
)

top_features = (
    feature_df
    .sort_values(
        "absolute_coefficient",
        ascending=False
    )
    .head(15)
)

fig3 = px.bar(
    top_features,
    x="absolute_coefficient",
    y="feature",
    orientation="h",
    title="Top 15 Feature Importance Drivers"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

feature_csv = top_features.to_csv(
    index=False
)

st.download_button(
    "📥 Download Feature Importance",
    feature_csv,
    "feature_importance.csv",
    "text/csv"
)

st.divider()

# =====================================================
# Model Comparison Metrics
# =====================================================

st.subheader(
    "Model Comparison Metrics"
)

comparison_df = model_df.copy()

comparison_df = comparison_df[
    [
        "model_name",
        "cv_rmse",
        "test_rmse",
        "test_mae",
        "test_r2",
        "r2_gap",
        "rmse_gap"
    ]
]

comparison_df.columns = [
    "Model",
    "CV RMSE",
    "Test RMSE",
    "Test MAE",
    "Test R²",
    "R² Gap",
    "RMSE Gap"
]

st.dataframe(
    comparison_df,
    use_container_width=True
)

# =====================================================
# Model Interpretation Summary
# =====================================================

st.subheader(
    "Model Interpretation Summary"
)

best_model = model_df.loc[
    model_df["test_r2"].idxmax()
]

summary_df = pd.DataFrame(
    {
        "Observation": [
            "Best Performing Model",
            "Test R²",
            "Test RMSE",
            "Test MAE",
            "Generalization"
        ],
        "Interpretation": [
            best_model["model_name"],
            round(best_model["test_r2"], 3),
            round(best_model["test_rmse"], 3),
            round(best_model["test_mae"], 3),
            (
                "Good"
                if abs(best_model["r2_gap"]) < 0.05
                else "Needs Review"
            )
        ]
    }
)

st.dataframe(
    summary_df,
    use_container_width=True,
    hide_index=True
)

# =====================================================
# Export Prediction Dataset
# =====================================================

st.subheader(
    "Export Prediction Dataset"
)

csv = prediction_df.to_csv(
    index=False
)

st.download_button(
    label="📥 Download Prediction Dataset",
    data=csv,
    file_name="prediction_dataset.csv",
    mime="text/csv"
)

st.divider()

# =====================================================
# Executive Insights Summary
# =====================================================

st.subheader(
    "Executive Insights Summary"
)

highest_department = (
    prediction_df
    .groupby("department")[
        "predicted_performance_score"
    ]
    .mean()
    .idxmax()
)

highest_score = round(
    prediction_df[
        "predicted_performance_score"
    ].max(),
    2
)

highest_employee = (
    prediction_df
    .sort_values(
        "predicted_performance_score",
        ascending=False
    )
    .iloc[0]
)

at_risk_count = len(
    prediction_df[
        prediction_df[
            "predicted_performance_score"
        ] < 3.0
    ]
)

top_feature = (
    feature_df
    .sort_values(
        "absolute_coefficient",
        ascending=False
    )
    .iloc[0]["feature"]
)

st.success(
    f"""
    Executive Summary

    • Highest Predicted Department: {highest_department}

    • Highest Predicted Employee:
      {highest_employee['first_name']} {highest_employee['last_name']}
      ({highest_score})

    • Total At-Risk Employees: {at_risk_count}

    • Most Influential Feature: {top_feature}

    • ElasticNet achieved the highest predictive performance and was selected as the final model.

    • Product department demonstrates the strongest predicted performance profile.

    • Technology contributes the largest workforce and salary cost, but is not the highest predicted performing department.

    • Operations, Procurement and Governance exhibit the most stable performance distributions.

    • Sales and Marketing show greater performance variability, indicating both high-performing and lower-performing employee groups.
    """
)

st.divider()

# =====================================================
# Business Recommendations
# =====================================================

st.subheader(
    "Business Recommendations"
)

recommendations = pd.DataFrame(
    {
        "Recommendation": [
            "Review Technology productivity",
            "Benchmark Product practices",
            "Focus intervention on At-Risk employees",
            "Monitor Sales variability",
            "Retain high-performing Delivery employees"
        ],
        "Business Rationale": [
            "Largest salary investment but not highest predicted performance",
            "Highest predicted department performance",
            "Reduce future performance risk",
            "Wide performance distribution detected",
            "Presence of exceptional performers"
        ]
    }
)

st.dataframe(
    recommendations,
    use_container_width=True,
    hide_index=True
)

st.divider()

# =====================================================
# Dataset Preview
# =====================================================

st.subheader(
    "Prediction Dataset Preview"
)

st.dataframe(
    prediction_df,
    use_container_width=True
)
