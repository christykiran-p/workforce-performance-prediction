import pandas as pd


def create_hierarchy_features(reporting_df: pd.DataFrame) -> pd.DataFrame:
    return (
        reporting_df
        .groupby("reporting_manager_id", as_index=False)
        .size()
        .rename(columns={
            "reporting_manager_id": "employee_id",
            "size": "team_size"
        })
    )