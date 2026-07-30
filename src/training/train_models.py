from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.evaluation.model_metrics import calculate_regression_metrics
from src.models.regression_models import get_regression_models


DATA_PATH = Path("data/processed/employee_analytics_dataset.parquet")
MODELS_PATH = Path("models")
REPORTS_PATH = Path("reports")

TARGET_COLUMN = "avg_performance_score"


DROP_COLUMNS = [
    "employee_id",
    "first_name",
    "last_name",
    "dob",
    "doj",
    "mobile_number",
    "emergency_contact",
    "email_id",
    "employee_termination_date",
    "exit_formalities_date",
    "created_at",
    "updated_at",
    "org_id",
    TARGET_COLUMN,
]


def load_training_data() -> pd.DataFrame:
    df = pd.read_parquet(DATA_PATH)

    # Remove rows where performance score is missing but represented as 0
    df = df[df[TARGET_COLUMN] > 0].copy()

    return df


def prepare_features_and_target(df: pd.DataFrame):
    y = df[TARGET_COLUMN]

    X = df.drop(columns=DROP_COLUMNS, errors="ignore")

    categorical_columns = X.select_dtypes(include=["object", "category"]).columns.tolist()
    numerical_columns = X.select_dtypes(include=["int64", "float64", "bool"]).columns.tolist()

    return X, y, categorical_columns, numerical_columns


def build_preprocessor(categorical_columns, numerical_columns):
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                StandardScaler(),
                numerical_columns,
            ),
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_columns,
            ),
        ]
    )

    return preprocessor


def train_and_evaluate_models():
    MODELS_PATH.mkdir(parents=True, exist_ok=True)
    REPORTS_PATH.mkdir(parents=True, exist_ok=True)

    df = load_training_data()

    X, y, categorical_columns, numerical_columns = prepare_features_and_target(df)

    print("Training dataset shape:", X.shape)
    print("Target rows:", len(y))
    print("Numerical columns:", numerical_columns)
    print("Categorical columns:", categorical_columns)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    preprocessor = build_preprocessor(
        categorical_columns,
        numerical_columns,
    )

    models = get_regression_models()

    results = []
    trained_models = {}

    for model_name, model in models.items():
        print(f"\nTraining model: {model_name}")

        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", model),
            ]
        )

        pipeline.fit(X_train, y_train)

        train_pred = pipeline.predict(X_train)
        test_pred = pipeline.predict(X_test)

        metrics = calculate_regression_metrics(
            y_train,
            train_pred,
            y_test,
            test_pred,
        )

        cv_scores = cross_val_score(
            pipeline,
            X,
            y,
            cv=5,
            scoring="neg_root_mean_squared_error",
        )

        cv_rmse = -cv_scores.mean()

        model_result = {
            "model_name": model_name,
            "cv_rmse": cv_rmse,
            **metrics,
        }

        results.append(model_result)
        trained_models[model_name] = pipeline

        model_file_name = model_name.lower().replace(" ", "_") + ".pkl"
        model_path = MODELS_PATH / model_file_name

        joblib.dump(pipeline, model_path)

        print(f"Saved model -> {model_path}")
        print(model_result)

    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(
        by="test_rmse",
        ascending=True,
    )

    comparison_path = REPORTS_PATH / "model_comparison.csv"
    results_df.to_csv(comparison_path, index=False)

    best_model_name = results_df.iloc[0]["model_name"]
    best_model = trained_models[best_model_name]

    best_model_path = MODELS_PATH / "best_model.pkl"
    joblib.dump(best_model, best_model_path)

    print("\nModel comparison saved ->", comparison_path)
    print("Best model:", best_model_name)
    print("Best model saved ->", best_model_path)

    create_feature_importance_report(best_model, best_model_name, X)


def create_feature_importance_report(best_model, best_model_name, X):
    model = best_model.named_steps["model"]
    preprocessor = best_model.named_steps["preprocessor"]

    try:
        feature_names = preprocessor.get_feature_names_out()
    except Exception:
        feature_names = X.columns

    if hasattr(model, "feature_importances_"):
        importance_df = pd.DataFrame({
            "feature": feature_names,
            "importance": model.feature_importances_,
        })

        importance_df = importance_df.sort_values(
            by="importance",
            ascending=False,
        )

        output_path = REPORTS_PATH / "feature_importance.csv"
        importance_df.to_csv(output_path, index=False)

        print("Feature importance saved ->", output_path)

    elif hasattr(model, "coef_"):
        importance_df = pd.DataFrame({
            "feature": feature_names,
            "coefficient": model.coef_,
        })

        importance_df["absolute_coefficient"] = (
            importance_df["coefficient"].abs()
        )

        importance_df = importance_df.sort_values(
            by="absolute_coefficient",
            ascending=False,
        )

        output_path = REPORTS_PATH / "feature_importance.csv"
        importance_df.to_csv(output_path, index=False)

        print("Feature coefficient report saved ->", output_path)

    else:
        print(
            f"Feature importance not available for best model: {best_model_name}"
        )


if __name__ == "__main__":
    train_and_evaluate_models()