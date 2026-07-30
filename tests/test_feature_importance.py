import pandas as pd


def test_feature_importance_exists():

    df = pd.read_csv(
        "reports/feature_importance.csv"
    )

    assert len(df) > 0


def test_feature_column_exists():

    df = pd.read_csv(
        "reports/feature_importance.csv"
    )

    assert "feature" in df.columns


def test_importance_column_exists():

    df = pd.read_csv(
        "reports/feature_importance.csv"
    )

    assert (
        "absolute_coefficient"
        in df.columns
    )