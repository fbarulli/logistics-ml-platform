from .lightgbm import LightGBMModel
from .xgboost import XGBoostModel

MODELS = {
    "lightgbm": LightGBMModel,
    "xgboost": XGBoostModel,
}


def get_model(name: str, **params):

    if name not in MODELS:
        raise ValueError(f"Unknown model '{name}'")

    return MODELS[name](**params)
