"""
ML model training for variant actionability scoring.
- Loads engineered features from data/engineered_variants.csv
- Simulates a target label (actionability_score)
- Trains an XGBoost regressor
- Saves the model to models/xgb_model.pkl
"""
import pandas as pd
import xgboost as xgb
import joblib
import os
import numpy as np


def train_model(input_csv, model_path):
    df = pd.read_csv(input_csv)
    # Simulate a target label (for demo)
    np.random.seed(42)
    df["actionability_score"] = (
        60 + 20 * df["hotspot_flag"] + 10 * df["driver_gene_flag"] +
        df["tmb"].astype(float) + np.random.normal(0, 5, len(df))
    ).astype(int)
    features = [
        "hotspot_flag", "driver_gene_flag", "tmb", "tumor_type_encoded"
    ]
    X = df[features]
    y = df["actionability_score"]
    model = xgb.XGBRegressor(n_estimators=50, random_state=42, base_score=60.0)
    model.fit(X, y)
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    # Save Booster directly for SHAP compatibility
    json_path = model_path.replace('.pkl', '.json')
    model.get_booster().save_model(json_path)
    print(f"Model trained and saved to {json_path}")

if __name__ == "__main__":
    input_csv = os.path.join(os.path.dirname(__file__), "../../data/engineered_variants.csv")
    model_path = os.path.join(os.path.dirname(__file__), "../../models/xgb_model.pkl")
    train_model(input_csv, model_path)
