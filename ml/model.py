# XGBoost model loading, scoring, and SHAP explainability

import xgboost as xgb
import shap
import numpy as np

class VariantScoringModel:
    def __init__(self, model_path: str):
        self.model = xgb.Booster()
        self.model.load_model(model_path)
        self.explainer = shap.TreeExplainer(self.model)

    def predict(self, features: np.ndarray):
        score = self.model.predict(xgb.DMatrix(features))
        shap_values = self.explainer.shap_values(features)
        return score, shap_values
