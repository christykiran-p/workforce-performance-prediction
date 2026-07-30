import pandas as pd


def test_model_comparison_exists():

    df = pd.read_csv(
        "reports/model_comparison.csv"
    )

    assert len(df) > 0


def test_best_model_exists():

    df = pd.read_csv(
        "reports/model_comparison.csv"
    )

    assert (
        "model_name"
        in df.columns
    )


def test_r2_column_exists():

    df = pd.read_csv(
        "reports/model_comparison.csv"
    )

    assert (
        "test_r2"
        in df.columns
    )