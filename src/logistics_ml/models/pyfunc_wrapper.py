from __future__ import annotations

import mlflow.pyfunc
import pandas as pd

from logistics_ml.features import FeaturePipeline
from logistics_ml.models.base import BaseModel


class TaxiDurationPyfuncModel(mlflow.pyfunc.PythonModel):
    """
    Bundles a fitted FeaturePipeline with a trained model so that
    raw trip data goes in and a duration prediction comes out.
    """

    def __init__(self, feature_pipeline: FeaturePipeline, model: BaseModel):
        self.feature_pipeline = feature_pipeline
        self.model = model

    def predict(self, context, model_input: pd.DataFrame, params=None):
        features = self.feature_pipeline.transform(model_input)
        return self.model.predict(features)
