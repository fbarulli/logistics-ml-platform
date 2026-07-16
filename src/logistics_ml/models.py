from lightgbm import LGBMRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor

from logistics_ml.config import RANDOM_STATE


def get_pipeline(model_name: str) -> Pipeline:
    models = {
        "linear": LinearRegression(),
        "rf": RandomForestRegressor(
            n_estimators=100,
            max_depth=20,
            max_samples=0.3,
            n_jobs=-1,
            random_state=RANDOM_STATE,
        ),
        "xgb": XGBRegressor(
            n_estimators=300,
            max_depth=6,
            learning_rate=0.1,
            tree_method="hist",
            n_jobs=-1,
            random_state=RANDOM_STATE,
        ),
        "lgbm": LGBMRegressor(
            n_estimators=300,
            learning_rate=0.1,
            n_jobs=-1,
            random_state=RANDOM_STATE,
        ),
    }

    if model_name not in models:
        raise ValueError(f"Unknown model: {model_name}")

    return Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("model", models[model_name]),
    ])
