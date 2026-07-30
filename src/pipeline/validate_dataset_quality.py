from pathlib import Path

import pandas as pd


PROCESSED_PATH = Path("data/processed")


def validate_dataset_quality() -> None:

    dataset_path = (
        PROCESSED_PATH /
        "employee_analytics_dataset.parquet"
    )

    df = pd.read_parquet(dataset_path)

    print("\nDATASET SHAPE")
    print(df.shape)

    print("\nTOTAL NULL VALUES")
    print(df.isnull().sum())

    print("\nDUPLICATE EMPLOYEE IDs")
    duplicate_count = df["employee_id"].duplicated().sum()
    print(f"Duplicate employee_id count: {duplicate_count}")

    print("\nEMPLOYEES WITH MISSING PERFORMANCE")
    missing_perf = (
        df["avg_performance_score"] == 0
    ).sum()
    print(f"Employees missing performance score: {missing_perf}")

    print("\nEMPLOYEES WITH LOW ATTENDANCE")
    low_attendance = (
        df["attendance_rate"] < 40
    ).sum()
    print(f"Employees below 40% attendance: {low_attendance}")

    print("\nEMPLOYEES WITH HIGH OVERTIME")
    high_ot = (
        df["total_overtime_hours"] > 100
    ).sum()
    print(f"Employees with overtime > 100 hours: {high_ot}")

    print("\nEMPLOYEES WITHOUT MANAGED TEAM")
    no_team = (
        df["team_size"] == 0
    ).sum()
    print(f"Employees without team members: {no_team}")

    print("\nTOP 5 DEPARTMENTS BY PERFORMANCE")
    print(
        df.groupby("department")[
            "avg_performance_score"
        ]
        .mean()
        .sort_values(ascending=False)
        .head(5)
    )


if __name__ == "__main__":
    validate_dataset_quality()