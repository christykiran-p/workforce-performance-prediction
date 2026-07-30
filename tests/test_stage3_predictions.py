import pandas as pd


def test_prediction_file_exists():

    df = pd.read_csv(
        "reports/prediction_output.csv"
    )

    assert df is not None
    assert len(df) > 0


def test_prediction_column_exists():

    df = pd.read_csv(
        "reports/prediction_output.csv"
    )

    assert (
        "predicted_performance_score"
        in df.columns
    )


def test_predictions_generated():

    df = pd.read_csv(
        "reports/prediction_output.csv"
    )

    prediction_count = (
        df[
            "predicted_performance_score"
        ]
        .notna()
        .sum()
    )

    assert prediction_count > 0


def test_prediction_categories_exist():

    df = pd.read_csv(
        "reports/prediction_output.csv"
    )

    assert (
        "prediction_category"
        in df.columns
    )