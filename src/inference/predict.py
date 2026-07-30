from pathlib import Path

import joblib
import pandas as pd

from src.ai.report.report_generator import AIReportGenerator

from src.config.settings import (
    DATA_PATH,
    MODEL_PATH,
    OUTPUT_PATH,
)

TARGET_COLUMN = "avg_performance_score"

DROP_COLUMNS = [
    "employee_id",
    "first_name",
    "last_name",
    "dob",
    "doj",
    "mobile_number",
    "emergency_contact",
    "email_id",
    "employee_termination_date",
    "exit_formalities_date",
    "created_at",
    "updated_at",
    "org_id",
    TARGET_COLUMN,
]


def load_model():
    return joblib.load(MODEL_PATH)


def load_prediction_data() -> pd.DataFrame:
    df = pd.read_parquet(DATA_PATH)
    return df.copy()


def prepare_prediction_features(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(columns=DROP_COLUMNS, errors="ignore")


def assign_performance_category(score: float) -> str:
    """Assign a human-readable category to the predicted score."""

    if pd.isna(score):
        return "Prediction Unavailable"

    if score >= 4.0:
        return "High Performer"

    if score >= 3.0:
        return "Consistent Performer"

    if score >= 2.0:
        return "Needs Improvement"

    return "Critical Attention"


def generate_predictions() -> None:

    # ----------------------------------------
    # Load Model & Data
    # ----------------------------------------

    model = load_model()

    df = load_prediction_data()

    X = prepare_prediction_features(df)

    predictions = model.predict(X)

    # ----------------------------------------
    # Prediction Output
    # ----------------------------------------

    output_df = df[
        [
            "employee_id",
            "first_name",
            "last_name",
            "department",
            "job_title",
            "avg_performance_score",
        ]
    ].copy()

    output_df["predicted_performance_score"] = predictions

    output_df["prediction_category"] = (
        output_df["predicted_performance_score"]
        .apply(assign_performance_category)
    )

    

    # ----------------------------------------
    # Save Prediction Report
    # ----------------------------------------

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_df.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(f"\nPrediction output saved -> {OUTPUT_PATH}")

    print(output_df.head(10))


if __name__ == "__main__":
    generate_predictions()