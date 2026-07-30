from pathlib import Path

import pandas as pd

from src.features.attendance_features import create_attendance_features
from src.features.hierarchy_features import create_hierarchy_features
from src.features.leave_features import create_leave_features
from src.features.performance_features import create_performance_features


RAW_PATH = Path("data/raw")
PROCESSED_PATH = Path("data/processed")


def load_parquet(table_name: str) -> pd.DataFrame:
    path = RAW_PATH / f"{table_name}.parquet"
    return pd.read_parquet(path)


def build_analytical_dataset() -> None:
    employee_df = load_parquet("employee")
    performance_df = load_parquet("employee_performance")
    attendance_df = load_parquet("employee_attendance")
    leave_df = load_parquet("leave_balance")
    reporting_df = load_parquet("employee_reporting")

    performance_features = create_performance_features(performance_df)
    attendance_features = create_attendance_features(attendance_df)
    leave_features = create_leave_features(leave_df)
    hierarchy_features = create_hierarchy_features(reporting_df)

    analytical_df = employee_df.copy()

    analytical_df = analytical_df.merge(
        performance_features,
        on="employee_id",
        how="left"
    )

    analytical_df = analytical_df.merge(
        attendance_features,
        on="employee_id",
        how="left"
    )

    analytical_df = analytical_df.merge(
        leave_features,
        on="employee_id",
        how="left"
    )

    analytical_df = analytical_df.merge(
        hierarchy_features,
        on="employee_id",
        how="left"
    )

    # ----------------------------------------------------
    # Department Owners / Functional Heads
    # Employee IDs 1-7 are exempt from performance reviews
    #
    # Keep performance fields as NULL
    # Do NOT convert to 0
    # ----------------------------------------------------

    fill_zero_columns = [
        "attendance_rate",
        "avg_working_hours",
        "total_overtime_hours",
        "total_shortfall_hours",
        "total_privileged_leave_used",
        "total_sick_leave_used",
        "total_lop_days",
        "avg_total_leave_balance",
        "total_leave_used",
        "team_size",
    ]

    for column in fill_zero_columns:
        if column in analytical_df.columns:
            analytical_df[column] = analytical_df[column].fillna(0)

    PROCESSED_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = (
        PROCESSED_PATH /
        "employee_analytics_dataset.parquet"
    )

    analytical_df.to_parquet(
        output_path,
        index=False
    )

    print(f"Processed dataset saved -> {output_path}")
    print(f"Total rows: {len(analytical_df)}")
    print(f"Total columns: {len(analytical_df.columns)}")
    print("Columns:")
    print(analytical_df.columns.tolist())


if __name__ == "__main__":
    build_analytical_dataset()