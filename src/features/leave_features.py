import pandas as pd


def create_leave_features(leave_df: pd.DataFrame) -> pd.DataFrame:
    leave_summary = (
        leave_df
        .groupby("employee_id", as_index=False)
        .agg({
            "privileged_leave_used": "sum",
            "sick_leave_used": "sum",
            "lop_days": "sum",
            "total_leave_balance": "mean"
        })
        .rename(columns={
            "privileged_leave_used": "total_privileged_leave_used",
            "sick_leave_used": "total_sick_leave_used",
            "lop_days": "total_lop_days",
            "total_leave_balance": "avg_total_leave_balance"
        })
    )

    leave_summary["total_leave_used"] = (
        leave_summary["total_privileged_leave_used"]
        + leave_summary["total_sick_leave_used"]
        + leave_summary["total_lop_days"]
    )

    return leave_summary