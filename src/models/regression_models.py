from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor


def get_regression_models():
    return {
        "Linear Regression": LinearRegression(),

        "Ridge Regression": Ridge(alpha=1.0, random_state=42),

        "Lasso Regression": Lasso(alpha=0.01, random_state=42, max_iter=10000),

        "ElasticNet Regression": ElasticNet(
            alpha=0.01,
            l1_ratio=0.5,
            random_state=42,
            max_iter=10000
        ),

        "Decision Tree": DecisionTreeRegressor(
            random_state=42,
            max_depth=5
        ),

        "Random Forest": RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            max_depth=8
        ),

        "XGBoost": XGBRegressor(
            n_estimators=100,
            learning_rate=0.05,
            max_depth=4,
            random_state=42,
            objective="reg:squarederror"
        ),
    }