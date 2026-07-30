from pathlib import Path

import pandas as pd


def test_processed_dataset_exists():
    path = Path("data/processed/employee_analytics_dataset.parquet")
    assert path.exists()


def test_processed_dataset_has_rows():
    path = Path("data/processed/employee_analytics_dataset.parquet")
    df = pd.read_parquet(path)

    assert len(df) > 0
    assert "employee_id" in df.columns


def test_processed_dataset_has_engineered_features():
    path = Path("data/processed/employee_analytics_dataset.parquet")
    df = pd.read_parquet(path)

    expected_features = [
        "avg_performance_score",
        "attendance_rate",
        "total_leave_used",
        "team_size",
    ]

    for feature in expected_features:
        assert feature in df.columns


def test_no_duplicate_employee_ids():
    path = Path("data/processed/employee_analytics_dataset.parquet")
    df = pd.read_parquet(path)

    assert df["employee_id"].duplicated().sum() == 0