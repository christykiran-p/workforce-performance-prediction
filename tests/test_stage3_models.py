import pandas as pd

from src.evaluation.model_metrics import calculate_regression_metrics
from src.inference.predict import assign_performance_category
from src.models.regression_models import get_regression_models
from src.training.train_models import (
    TARGET_COLUMN,
    load_training_data,
    prepare_features_and_target,
)

from src.inference.predict import (
    load_prediction_data,
    prepare_prediction_features,
)
from src.training.train_models import build_preprocessor

from pathlib import Path

from src.training.train_models import train_and_evaluate_models
from src.inference.predict import generate_predictions

def test_get_regression_models():
    models = get_regression_models()

    expected_models = [
        "Linear Regression",
        "Ridge Regression",
        "Lasso Regression",
        "ElasticNet Regression",
        "Decision Tree",
        "Random Forest",
        "XGBoost",
    ]

    for model_name in expected_models:
        assert model_name in models


def test_calculate_regression_metrics():
    y_train = [3.0, 4.0, 5.0]
    train_pred = [3.1, 3.9, 4.8]

    y_test = [3.5, 4.5]
    test_pred = [3.4, 4.6]

    metrics = calculate_regression_metrics(
        y_train,
        train_pred,
        y_test,
        test_pred,
    )

    expected_keys = [
        "train_rmse",
        "test_rmse",
        "train_mae",
        "test_mae",
        "train_r2",
        "test_r2",
        "r2_gap",
        "rmse_gap",
    ]

    for key in expected_keys:
        assert key in metrics


def test_assign_performance_category():
    assert assign_performance_category(4.2) == "High Performer"
    assert assign_performance_category(3.5) == "Consistent Performer"
    assert assign_performance_category(2.5) == "Needs Improvement"
    assert assign_performance_category(1.5) == "Critical Attention"


def test_load_training_data_removes_zero_scores():
    df = load_training_data()

    assert len(df) > 0
    assert (df[TARGET_COLUMN] == 0).sum() == 0


def test_prepare_features_and_target():
    df = load_training_data()

    X, y, categorical_columns, numerical_columns = prepare_features_and_target(df)

    assert TARGET_COLUMN not in X.columns
    assert len(X) == len(y)
    assert len(categorical_columns) > 0
    assert len(numerical_columns) > 0

def test_load_prediction_data():
    df = load_prediction_data()

    assert len(df) > 0
    assert "employee_id" in df.columns
    assert "avg_performance_score" in df.columns


def test_prepare_prediction_features():
    df = load_prediction_data()

    X = prepare_prediction_features(df)

    assert "avg_performance_score" not in X.columns
    assert "employee_id" not in X.columns
    assert len(X) == len(df)

def test_build_preprocessor():
    df = load_training_data()

    X, y, categorical_columns, numerical_columns = prepare_features_and_target(df)

    preprocessor = build_preprocessor(
        categorical_columns,
        numerical_columns,
    )

    transformed = preprocessor.fit_transform(X)

    assert transformed.shape[0] == len(X)

def test_train_and_evaluate_models_integration():
    train_and_evaluate_models()

    assert Path("models/best_model.pkl").exists()
    assert Path("reports/model_comparison.csv").exists()
    assert Path("reports/feature_importance.csv").exists()


def test_generate_predictions_integration():
    generate_predictions()

    assert Path("reports/prediction_output.csv").exists()