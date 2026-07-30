import pandas as pd


def create_performance_features(performance_df: pd.DataFrame) -> pd.DataFrame:
    return (
        performance_df
        .groupby("employee_id", as_index=False)
        .agg({
            "overall_score": "mean",
            "bonus_percentage": "mean"
        })
        .rename(columns={
            "overall_score": "avg_performance_score",
            "bonus_percentage": "avg_bonus_percentage"
        })
    )