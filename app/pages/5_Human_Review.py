import streamlit as st
import pandas as pd
from pathlib import Path

from src.config.settings import DATA_PATH
from src.ai.report.report_generator import AIReportGenerator
from src.hitl.workflow import HITLWorkflow


st.set_page_config(
    page_title="Human Review",
    page_icon="👨‍💼",
    layout="wide",
)

st.title("👨‍💼 Human-in-the-Loop Review")


# =====================================================
# Load Prediction Output
# =====================================================

@st.cache_data
def load_predictions():
    file_path = Path("reports/prediction_output.csv")

    if not file_path.exists():
        return pd.DataFrame()

    return pd.read_csv(file_path)


@st.cache_data
def load_employee_data():
    return pd.read_parquet(DATA_PATH)


prediction_df = load_predictions()
employee_df = load_employee_data()

if prediction_df.empty:
    st.warning("No prediction records found.")
    st.stop()


# =====================================================
# Validate Required Columns
# =====================================================

required_columns = [
    "employee_id",
    "first_name",
    "last_name",
    "department",
    "job_title",
    "predicted_performance_score",
    "prediction_category",
]

missing_columns = [
    col
    for col in required_columns
    if col not in prediction_df.columns
]

if missing_columns:
    st.error(
        f"Missing columns in prediction_output.csv:\n\n{missing_columns}"
    )
    st.stop()


# =====================================================
# Employee Selection
# =====================================================

employee_options = (
    prediction_df["employee_id"].astype(str)
    + " - "
    + prediction_df["first_name"]
    + " "
    + prediction_df["last_name"]
)

selected_employee = st.selectbox(
    "Select Employee",
    employee_options,
)

employee_id = int(selected_employee.split(" - ")[0])

employee = prediction_df[
    prediction_df["employee_id"] == employee_id
].iloc[0]


# =====================================================
# Employee Information
# =====================================================

st.divider()

st.subheader("Employee Information")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("**Employee ID**")
    st.write(employee["employee_id"])

with col2:
    st.write("**Employee Name**")
    st.write(
        f"{employee['first_name']} {employee['last_name']}"
    )

with col3:
    st.write("**Department**")
    st.write(employee["department"])

st.write("**Job Title**")
st.write(employee["job_title"])


# =====================================================
# Prediction Summary
# =====================================================

st.divider()

st.subheader("Prediction Summary")

col1, col2 = st.columns(2)

with col1:

    score = employee["predicted_performance_score"]

    if pd.isna(score):

        st.metric(
            "Predicted Score",
            "N/A",
        )

    else:

        st.metric(
            "Predicted Score",
            round(float(score), 2),
        )

with col2:

    st.metric(
        "Prediction Category",
        employee["prediction_category"],
    )


# =====================================================
# AI Insights
# =====================================================

st.divider()

st.subheader("AI Insights")

if "ai_report" not in st.session_state:
    st.session_state.ai_report = None

if st.button(
    "Generate AI Insights",
    use_container_width=True,
):

    with st.spinner("Generating AI Insights..."):

        generator = AIReportGenerator(employee_df)

        st.session_state.ai_report = generator.generate(
            employee_id=int(employee["employee_id"]),
            predicted_score=employee["predicted_performance_score"],
            category=employee["prediction_category"],
        )

if st.session_state.ai_report:

    report = st.session_state.ai_report

    with st.expander(
        "AI Explanation",
        expanded=True,
    ):
        st.info(
            " | ".join(
                report["explanation"]["summary"]
            )
        )

    with st.expander(
        "AI Recommendation",
        expanded=True,
    ):
        st.success(
            " | ".join(
                report["recommendations"]
            )
        )

    with st.expander(
        "AI Summary",
        expanded=True,
    ):
        st.write(report["summary"])


# =====================================================
# Reviewer Decision
# =====================================================

st.divider()

st.subheader("Reviewer Decision")

reviewer = st.text_input(
    "Reviewer Name",
    value=st.session_state.get(
        "username",
        "",
    ),
)

decision = st.radio(
    "Decision",
    [
        "Approved",
        "Rejected",
    ],
)

comments = st.text_area(
    "Comments",
    height=150,
)


# =====================================================
# Submit Review
# =====================================================

if st.button(
    "Submit Review",
    type="primary",
    use_container_width=True,
):

    workflow = HITLWorkflow()

    workflow.execute(
        employee_id=int(employee["employee_id"]),
        employee_name=f"{employee['first_name']} {employee['last_name']}",
        department=employee["department"],
        predicted_score=employee["predicted_performance_score"],
        prediction_category=employee["prediction_category"],
        reviewer=reviewer,
        decision=decision,
        comments=comments,
    )

    st.success("✅ Review submitted successfully.")

    st.balloons()


# =====================================================
# Review History
# =====================================================

history_file = Path("output/hitl_decisions.csv")

if history_file.exists():

    st.divider()

    st.subheader("Review History")

    history_df = pd.read_csv(history_file)

    st.dataframe(
        history_df,
        use_container_width=True,
    )