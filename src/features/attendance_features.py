import pandas as pd


def create_attendance_features(
    attendance_df: pd.DataFrame
) -> pd.DataFrame:

    attendance_df = attendance_df.copy()

    attendance_df["attendance_status"] = (
        attendance_df["attendance_status"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Remove non-working days

    attendance_df = attendance_df[
        ~attendance_df["attendance_status"].isin(
            ["weekend", "holiday"]
        )
    ]

    # Attendance scoring

    attendance_df["attendance_points"] = (
        attendance_df["attendance_status"]
        .map({
            "present": 1.0,
            "wfh": 1.0,
            "half-day": 0.5,
            "on-leave": 0.0,
            "absent": 0.0
        })
        .fillna(0)
    )

    attendance_summary = (
        attendance_df
        .groupby("employee_id", as_index=False)
        .agg({
            "attendance_points": "mean",
            "total_working_hours": "mean",
            "overtime_hours": "sum",
            "shortfall_hours": "sum"
        })
        .rename(columns={
            "attendance_points": "attendance_rate",
            "total_working_hours": "avg_working_hours",
            "overtime_hours": "total_overtime_hours",
            "shortfall_hours": "total_shortfall_hours"
        })
    )

    attendance_summary["attendance_rate"] = (
        attendance_summary["attendance_rate"] * 100
    )

    return attendance_summary